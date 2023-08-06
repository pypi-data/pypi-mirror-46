from __future__ import print_function

import datetime
import logging
import os
import re
import sys

import pprint as pp
import urllib
import magic
import easyprocess
import pathos
import pydicom
import requests
from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
from urllib3.util.retry import Retry
import natsort
import json
import jsbeautifier


class XnatUploadToolDicom:
    def __init__(self, **kwargs):
        # Designed to be called from script using argparse, otherwise dict must be passed in as kwargs with
        # all following variables set
        try:
            self.args = kwargs
            self.starttime = None
            self.httpsess = None
            self.lastrenew = None
            self.logger = None
            self.prearcdate = False
            self.host = kwargs['host'].rstrip('/')
            self.localval = dict()
            self.upload_time = int()
            self.build_time = int()
            self.archive_time = int()
            self.verbose = kwargs['verbose']
            self.logfile = kwargs['logfile']

            self.fullmap = dict()

            self.dircount = 0
            self.filecount = 0
            self.uploadcount = 0
            self.newsessions = 0
            self.newscans = 0
            self.newuploads = 0

            self.uploadtree = list()
            self.filetree = dict()
            self.fullmap = dict()
            self.checked_values = {'projects': {}}
            self.sessionmap = {'projects': {}}

            # Pull u/p from env if not set in args
            if kwargs['username'] is None or kwargs['password'] is None:
                (self.username, self.password) = os.environ['XNATCREDS'].split(':', 2)
            else:
                self.username = kwargs['username']
                self.password = kwargs['password']

            self.timeout = kwargs['timeout']
            self.sessiontimeout = datetime.timedelta(minutes=kwargs['sessiontimeout'])

            if 'jobs' in kwargs and kwargs['jobs'] is not None:
                self.threads = kwargs['jobs']
            else:
                self.threads = 1
            self.project = kwargs['project']
            self.subject = kwargs['subject']
            self.projectlabel = kwargs['projectlabel']
            self.splitlabel = kwargs['splitlabel']
            self.deletesessions = kwargs['deletesessions']
            self.target = kwargs['target']
            self.splitsample = kwargs['splitsample']

            self.dumpmap = kwargs['dumpmap']

            # Set up logging
            self.setup_logger()

            tagmatch = re.compile("^\(([0-9a-fA-F]+),([0-9a-fA-F]+)\)$")

            if kwargs['splitlabel'] is not None and tagmatch.match(kwargs['splitlabel']) is not None:
                self.splitlabel = [hex(int(tagmatch.search(kwargs['splitlabel'].upper()).group(1), 16)),
                                   hex(int(tagmatch.search(kwargs['splitlabel'].upper()).group(2), 16))]

            if kwargs['projectlabel'] is not None and tagmatch.match(kwargs['projectlabel']) is not None:
                self.projectlabel = [hex(int(tagmatch.search(kwargs['projectlabel'].upper()).group(1), 16)),
                                     hex(int(tagmatch.search(kwargs['projectlabel'].upper()).group(2), 16))]

            if tagmatch.match(kwargs['subjectlabel']) is None:
                self.logger.error('Subject tag %s is not in valid format.' % kwargs['subjectlabel'])
                exit(1)
            else:
                self.subjectlabel = [hex(int(tagmatch.search(kwargs['subjectlabel'].upper()).group(1), 16)),
                                     hex(int(tagmatch.search(kwargs['subjectlabel'].upper()).group(2), 16))]

            if tagmatch.match(kwargs['sessionlabel']) is None:
                self.logger.error('Session tag %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                self.sessionlabel = [hex(int(tagmatch.search(kwargs['sessionlabel'].upper()).group(1), 16)),
                                     hex(int(tagmatch.search(kwargs['sessionlabel'].upper()).group(2), 16))]

            if tagmatch.match(kwargs['sessiondate']) is None:
                self.logger.error('Session date %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                self.sessiondate = [hex(int(tagmatch.search(kwargs['sessiondate'].upper()).group(1), 16)),
                                    hex(int(tagmatch.search(kwargs['sessiondate'].upper()).group(2), 16))]

            if tagmatch.match(kwargs['scandate']) is None:
                self.logger.error('Session date %s is not in valid format.' % self.sessionlabel)
                exit(1)
            else:
                self.scandate = [hex(int(tagmatch.search(kwargs['scandate'].upper()).group(1), 16)),
                                 hex(int(tagmatch.search(kwargs['scandate'].upper()).group(2), 16))]

            self.scanuid = ['0x20', '0xe']
            self.sessionuid = ['0x20', '0xd']
            self.scanlabel = ['0x20', '0x11']
            self.modality = ['0x8', '0x60']
            self.seriesdesc = ['0x8', '0x103e']
            self.studydesc = ['0x8', '0x1030']

            # Initialize Sessions
            self.renew_httpsession()
        except KeyError as e:
            logging.error('Unable to initialize uploader, missing argument: %s' % str(e))
            exit(1)

    def setup_logger(self):
        # Set up logging
        hdlr = None
        if self.logfile is not None:
            if os.path.exists(os.path.dirname(os.path.realpath(self.logfile))):
                hdlr = logging.FileHandler(self.logfile)
            else:
                logging.error('Log path %s does not exists' % str(self.logfile))
                exit(1)
        else:
            hdlr = logging.StreamHandler(sys.stdout)

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if self.splitsample:
            self.logger.setLevel(logging.NOTSET)
        return True

    def setup_upload(self):
        self.logger.info('Preparing for dicom upload of %s to %s as %s' % (self.target, self.host, self.username))
        if self.dumpmap:
            self.logger.info('Mapdump requested to %s, no files will be uploaded' % self.dumpmap)
        return True

    def start_upload(self):
        self.setup_upload()
        self.analyze_dir(self.target)

        if self.dumpmap:
            self.sessionmap_dump()
            exit(0)

        self.logger.info('Beginning dicom upload of %d valid files' % len(self.uploadtree))

        # Facilitate single threaded/parallel upload
        uploadcount = 0
        upsize = 0
        starttime = datetime.datetime.now()

        for thisdi in self.uploadtree:
            uploadcount += 1
            upsize += os.path.getsize(thisdi['path'])
            if uploadcount % 100 == 0:
                ebw = upsize/(datetime.datetime.now()-starttime).total_seconds()
                self.logger.info('File upload progress: %d/%d (%s @ %s/s)' % (uploadcount,
                                                                              len(self.uploadtree),
                                                                              self.bytes_format(upsize),
                                                                              self.bytes_format(ebw)))

            self.upload_scan(thisdi)

        # Tell server to pull headers from uploaded sessions
        self.server_pull_headers()

        ebw = upsize / (datetime.datetime.now() - starttime).total_seconds()
        self.logger.info('Upload complete. %d files uploaded (%s @ %s/s)' % (uploadcount, self.bytes_format(upsize),
                                                                             self.bytes_format(ebw)))


        return True

    def analyze_dir(self, directory):
        # Analyze directory tree to find map of uploadable files
        anasize = 0
        self.logger.debug('Analyzing from basepath %s' % self.target)
        self.filetree[directory] = dict()
        if os.path.exists(directory):
            for d, r, f in os.walk(directory):
                # Cycle through directories
                for subdir in r:
                    if subdir.startswith(".") is not True and subdir not in self.filetree:
                        self.dircount += 1
                        if self.dircount % 100 == 0:
                            self.logger.info('Directories scan progress: %d' % self.dircount)

                for subfile in f:
                    self.logger.debug('Analyzing %s' % os.path.relpath(os.path.join(d, subfile), self.target))
                    self.filecount += 1
                    anasize += os.path.getsize(os.path.join(d, subfile))
                    if self.filecount % 1000 == 0:
                        self.logger.info('Files scan progress: %d (%s)' % (self.filecount, self.bytes_format(anasize)))

                    if subfile.startswith('.'):
                        self.logger.debug('Hidden file %s skipped' % subfile)
                    else:
                        mysubdir = os.path.basename(os.path.normpath(d))
                        mypath = os.path.join(d, subfile)
                        mime_type = magic.from_file(mypath, mime=True)
                        if mime_type == 'application/dicom':
                            # Pull tags, if none skip file, logging in function
                            di = self.pull_dicom_tags(mypath)
                            if di is None:
                                continue

                            self.renew_httpsession()

                            self.uploadtree.append(di)
                            self.update_map(di)
                        else:
                            self.logger.debug("File %s non-dicom or archive: %s" % (
                                os.path.relpath(os.path.join(d, subfile), self.target), str(mime_type)))
                            if os.path.isfile(subfile):
                                print(mysubdir)
        else:
            self.logger.error('Directory %s does not exist' % (os.path.abspath(directory)))
            exit(1)

        self.logger.info('Found Total: Files: %d Directories: %d' % (self.filecount, self.dircount))

        return True

    def upload_scan(self, di=None):
        # Upload generic data files individually
        sumsize = os.path.getsize(di['path'])

        if sumsize == 0:
            self.logger.info('%s : no files suitable for transfer. Skipping' % os.path.relpath(di['path'], self.target))
            return False

        self.logger.debug('[%s] Uploading data file %s (%s) to [Proj %s Sub %s Sess %s] Dir: %s' %
                          (di['scanlabel'], os.path.relpath(di['path'], self.target), self.bytes_format(sumsize),
                           di['project'], di['subjectlabel'], di['sessionlabel'], os.path.dirname(di['path'])))

        # Should only happen if tags are bad
        if di['project'] is None or di['subjectlabel'] is None:
            self.logger.error('[%s] Cannot upload data file, Project or Subject is not set' % di['scanlabel'])
            return False

        if not self.check_upload_dependencies(di):
            return False

        bwstarttime = datetime.datetime.now()
        upstat = {'success': 0, 'total': 0}

        # Check if http session needs to be renewed prior to proceeding
        self.renew_httpsession()
        myurl = (self.host + "/data/projects/%s/subjects/%s/experiments/%s/scans/%s/resources/DICOM/files/%s"
                 "?format=json&event_reason=upload&update-stats=false" %
                 (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanlabel'], os.path.basename(di['path'])))

        mydata = {'dicomupload': (os.path.basename(di['path']), open(di['path'], 'rb'), 'application/dicom')}

        try:
            response = self.httpsess.post(url=myurl, files=mydata, timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout:
            self.logger.error("[%s] Failed to upload %s due to read timeout, increase default from %d" %
                              (di['scanlabel'], os.path.relpath(di['path'], self.target), self.timeout))
            return False
        except requests.exceptions.ConnectionError:
            self.logger.error("[%s] Failed to upload %s due to read timeout, increase default from %d" %
                              (di['scanlabel'], os.path.relpath(di['path'], self.target), self.timeout))
            return False

        upstat['total'] += 1
        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

        if response.status_code == 200:
            upstat['success'] += 1

            dups = 0
            try:
                mytxt = json.loads(response.text)
                if 'duplicates' in mytxt:
                    dups = len(mytxt['duplicates'])
            except Exception:
                pass

            self.logger.debug('[%s] Transferred %d/%d files /w %d duplicates (runtime %ds)' %
                              (di['scanlabel'], upstat['success'], upstat['total'], dups,
                               transtime))
        else:
            self.logger.error("[%s] Failed to upload %s (runtime %ds) Server response: %s/%s [%s %s %s %s]" %
                              (di['scanlabel'], os.path.relpath(di['path'], self.target), transtime,
                               response.status_code, response.reason, di['project'], di['subjectlabel'],
                               di['sessionlabel'],
                               di['scanuid']))

        return upstat['success'], upstat['total'], sumsize

    def check_upload_dependencies(self, di):
        # Check file upload dependencies
        # Check project existence, if not skip
        if not self.check_project(project=di['project']):
            self.logger.error('Project %s access denied, for file %s, skipping' %
                              (di['project'], os.path.relpath(di['path'], self.target)))
            return False

        # # Check subject existence
        if not self.check_subject(di=di, create=True):
            self.logger.error('Subject %s does not exist or cannot be created on %s/%s for file %s, skipping' %
                              (di['subjectlabel'], self.host, di['project'], os.path.relpath(di['path'], self.target)))
            return False

        # # Check for session/scan duplicates
        di = self.check_session(di)
        if not di:
            return False
        di = self.check_scan(di)
        if not di:
            return False

        return di

    def check_project(self, project=None):
        if not project:
            project = self.project
        # Checks project existence on server
        if project in self.checked_values['projects']:
            return True
        try:
            response = self.httpsess.get(self.host + '/data/archive/projects/%s?accessible=true' % project)
            if response.status_code == 200:
                # initialized checked lists to assure uniqueness
                self.checked_values['projects'][project] = {'subjects': list(),
                                                            'sessionuids': dict(),
                                                            'sessionlabels': dict(),
                                                            'scanuids': dict(),
                                                            'scanlabels': dict()}
                return True
        except Exception as e:
            self.logger.error('Error checking project existence %s', str(e))

        return False

    def check_subject(self, di=None, create=True):
        # Checks subject existence on server, create if requested
        if di['subjectlabel'] is None:
            if di['subject'] is not None:
                di['subjectlabel'] = self.subject
            else:
                self.logger.error('Subject is not set, required for this upload.')
                return False

        if di['project'] in self.checked_values['projects'] and \
                'subjects' not in self.checked_values['projects'][di['project']]:
            self.checked_values['projects'][di['project']]['subjects'] = list()

        if di['subjectlabel'] in self.checked_values['projects'][di['project']]['subjects']:
            return True

        try:
            response = self.httpsess.get(self.host + '/data/projects/%s/subjects/%s?format=json' %
                                         (di['project'], di['subjectlabel']))
            if response.status_code == 200:
                # Add subject to cache
                if di['subjectlabel'] not in self.checked_values['projects'][di['project']]['subjects']:
                    self.checked_values['projects'][di['project']]['subjects'].append(di['subjectlabel'])
                return True
        except Exception as e:
            self.logger.error('Error checking subject existence %s', str(e))

        if create is True:
            # create new subject
            response = self.httpsess.put(self.host + '/data/projects/%s/subjects/%s?format=json&event_reason=upload' %
                                         (di['project'], di['subjectlabel']))
            if response.status_code == 201 or response.status_code == 200:
                self.logger.debug('Created new subject %s' % di['subjectlabel'])
                # Add subject to cache
                self.checked_values['projects'][di['project']]['subjects'].append([di['subjectlabel']])
                return True
            else:
                self.logger.debug('Unable to create subject %s: %s' % (di['subjectlabel'], response.text))

        return False

    def check_session(self, di):
        # Checks session existence for project/subject, creates with proper fields if necessary

        # Create cache of sessionuid:{sessionlabel,exists} mapping
        # https://rair.avidrp.com/data/experiments?format=html&xsiType=xnat:imageSessionData
        # &UID=1.3.12.2.1107.5.2.32.35248.30000012031314395204600

        # Session data is not on di, fail
        if di['sessionuid'] is None or di['sessionlabel'] is None:
            self.logger.error('Session uid or label is not set, cannot be checked, required for this upload')
            return False

        # If uid in cache, use existing label
        if di['sessionuid'] in self.checked_values['projects'][di['project']]['sessionuids']:
            di['sessionlabel'] = self.checked_values['projects'][di['project']]['sessionuids'][di['sessionuid']]
            return di

        # Check for uid on server by label, if has proper uid combo add to cache and proceed
        mysessionlabels = self.get_session_by_uid(di)
        if mysessionlabels is not None:
            for thisresult in mysessionlabels:
                if di['sessionlabel'] == self.strip_invalid(thisresult['label']):
                    # Add to cache
                    self.checked_values['projects'][di['project']]['sessionuids'][thisresult['UID']] = \
                        di['sessionlabel']
                    self.checked_values['projects'][di['project']]['sessionlabels'][thisresult['label']] = \
                        di['sessionuid']
                    return di

        # New session label is last label use
        lastlabels = self.pull_last_label(di, 'session')
        if lastlabels is not None:
            di['sessionlabel'] = self.generate_dup_label(next(iter(lastlabels)))

            # Double checks in app for label existence, iterating until new label is found
            while self.get_session_by_label(di) is not None:
                di['sessionlabel'] = self.generate_dup_label(di['sessionlabel'])

        # Create session, return None of fail
        if not self.create_session(di):
            return None

        # Return created object
        return di

    def check_scan(self, di):
        # if (scan label is NEW)
        #     -- new
        #     scan
        # else
        #     if (series UID is NEW)
        #         -- new scan - iterate
        #         scan label to be unique
        #     else
        #         -- existing scan - append to

        # Check if scan exists, create if requested
        if di['scanlabel'] is None or di['scanuid'] is None:
            self.logger.error('Scan label or uid is not set, cannot be checked, required for this upload.')
            return None

        # If uid in cache, use existing label
        if di['scanuid'] in self.checked_values['projects'][di['project']]['scanuids']:
            di['scanlabel'] = self.checked_values['projects'][di['project']]['scanuids'][di['scanuid']]
            return di

        # Check for uid on server by label, if has proper uid combo add to cache and proceed
        myscanlabels = self.get_scan_by_label(di)
        if myscanlabels is not None:
            for thisresult in myscanlabels:
                if di['scanlabel'] == self.strip_invalid(thisresult['data_fields']['ID']):
                    # Add to cache
                    self.checked_values['projects'][di['project']]['scanuids'][di['scanuid']] = \
                        thisresult['data_fields']['ID']
                    self.checked_values['projects'][di['project']]['scanlabels'][thisresult['data_fields']['ID']] = \
                        di['scanuid']
                    return di

        # Checks scan existence for project/subject/session, creates with proper fields if necessary
        # New scan label is last label use
        lastlabels = self.pull_last_label(di, 'scan')
        if lastlabels is not None:
            di['scanlabel'] = self.generate_dup_label(next(iter(lastlabels)))

            # Double checks in app for label existence, iterating until new label is found
            while self.get_scan_by_label(di) is not None:
                di['scanlabel'] = self.generate_dup_label(di['scanlabel'])

        # Create scan, return None of fail
        if not self.create_scan(di):
            return None

        return di

    def get_session_by_uid(self, di):
        # Pulls list of sessions from host based on uid, returns list of sessions

        response = self.httpsess.get(
            self.host + '/data/experiments?format=json&columns=project,subject_label,label,UID&'
                        'xsiType=xnat:imageSessionData&project=%s&UID=%s' %
            (di['project'], di['sessionuid']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull session by uid: response %s' % response.status_code)
        return None

    def get_session_by_label(self, di):
        # Pulls list of sessions from host based on label, returns list of sessions
        response = self.httpsess.get(
            self.host + '/data/experiments?format=json&columns=project,subject_label,label,UID&'
                        'xsiType=xnat:imageSessionData&project=%s&label=%s' %
            (di['project'], di['sessionlabel']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull session %s by label: response %s' % (di['sessionlabel'],
                                                                                   response.status_code))
        return None

    def get_scan_by_uid(self, di):
        # Pulls list of scans from host based on uid, returns list of sessions

        response = self.httpsess.get(
            self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/?format=json&UID=%s' %
            (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanuid']))

        if response.status_code == 200:
            if int(response.json()['ResultSet']['totalRecords']) == 0:
                return None
            else:
                return response.json()['ResultSet']['Result']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull scan %s by uid: response %s' % (di['scanlabel'], response.status_code))
        return None

    def get_scan_by_label(self, di):
        # Pulls list of scans from host based on label, returns list of scan
        response = self.httpsess.get(
            self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s?format=json' %
            (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanlabel']))

        if response.status_code == 200:
            if len(response.json()['items']) == 0:
                return None
            else:
                return response.json()['items']
        elif response.status_code == 404:
            return None
        else:
            # Error on request
            self.logger.error('Unable to pull scan %s by uid: response %s' % (di['scanlabel'], response.status_code))
        return None

    def pull_last_label(self, di, labeltype):
        # Search by label

        # Search for cached labels matching pattern
        result = []
        for key in self.checked_values['projects'][di['project']][labeltype + 'labels']:
            if key.startswith(di[labeltype + 'label']):
                result.append((key, self.checked_values['projects'][di['project']][(labeltype + 'labels')][key]))
        if len(result) == 0:
            return None
        else:
            return natsort.natsorted(result)[-1]

    def pull_last_scanlabel(self, di, labeltype):
        # Search by label
        # TODO : Need to change to search at project/subject/session level.

        # Search for cached labels matching pattern
        result = []
        for key in self.checked_values['projects'][di['project']]['subjects'][di['subjectlabel']][labeltype + 'labels']:
            if key.startswith(di[labeltype + 'label']):
                result.append((key, self.checked_values['projects'][di['project']][(labeltype + 'labels')][key]))

        if len(result) == 0:
            return None
        else:
            return natsort.natsorted(result)[-1]

    def generate_dup_label(self, label):
        labelnum = re.findall(r'_(\d+)$', label)
        if len(labelnum) > 0:
            # Increment existing dup count
            newlabel = re.sub(r'_' + labelnum[0] + '$', '_' + str(int(labelnum[0]) + 1), label)
            return newlabel
        else:
            # Add _1 since no previous dup count
            return label + '_1'

    def create_session(self, di):
        self.renew_httpsession()

        # If delete session is true, delete prior to create
        if self.deletesessions is True:
            self.delete_session(di)

        mymodality = self.get_session_modality(di['project'], di['subjectlabel'], di['sessionlabel'])

        params = {
            'xsiType': ('xnat:%s' % mymodality + 'SessionData'),
            'UID': di['sessionuid'],
            'label': di['sessionuid'],
            'date': str(di['sessiondate']),
            'note': str(di['scandesc']),
            'modality': mymodality.upper()
        }

        # Creates new session on host for project/subject
        response = self.httpsess.post(self.host + '/data/archive/projects/%s/subjects/%s/experiments/'
                                                  '?activate=true&label=%s&event_reason=upload' %
                                      (di['project'], di['subjectlabel'], di['sessionlabel']), params=params)

        if response.status_code == 200:
            self.logger.debug('Session %s created with uid %s as %s' % (di['sessionlabel'],
                                                                        di['sessionuid'],
                                                                        di['modality']))
            # Add to cache
            self.checked_values['projects'][di['project']]['sessionuids'][di['sessionuid']] = di['sessionlabel']
            self.newsessions += 1
        else:
            self.logger.debug('Unable to create session %s with uid %s on project %s as %s' %
                              (di['sessionlabel'], di['sessionuid'], di['project'], di['modality']))
            return False

        self.checked_values['projects'][di['project']]['sessionuids'][di['sessionuid']] = di['sessionlabel']
        self.checked_values['projects'][di['project']]['sessionlabels'][di['sessionlabel']] = di['sessionuid']

        return True

    def delete_session(self, di):
        # Delete session by uid

        response = self.httpsess.delete(self.host + "/data/projects/%s/subjects/%s/experiments/%s"
                                        "?removeFiles=true&event_action=ScriptedDeletion" % (
                                             di['project'],
                                             di['subjectlabel'],
                                             di['sessionlabel']
                                         ))

        if response.status_code == 404:
            return True
        elif response.status_code == 200:
            if self.verbose:
                self.logger.debug('Deleted existing project %s session %s/%s' % (di['project'], di['sessionlabel'],
                                                                                 di['sessionuid']))
                return True

        else:
            self.logger.debug('Unable to delete existing project %s session %s/%s: %s' % (di['project'],
                                                                                          di['sessionlabel'],
                                                                                          di['sessionuid'],
                                                                                          response.reason))
            return False

        return False

    def create_scan(self, di):
        # Creates new session on host for project/subject
        self.renew_httpsession()

        params = {
            'xsiType': ('xnat:%sScanData' % di['modality']),
            'UID': di['scanuid'],
            ('xnat:%sScanData/type' % di['modality']): str(di['scandesc']),
            ('xnat:%sScanData/series_description' % di['modality']): str(di['scandesc']),
            'xnat:imageScanData/modality': di['modality'].upper()
        }

        response = self.httpsess.put(self.host + '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s'
                                     '?event_reason=upload' %
                                     (di['project'], di['subjectlabel'], di['sessionlabel'], di['scanlabel']),
                                     params=params)

        if response.status_code == 200:
            self.logger.debug('Scan %s created with uid %s as %s' % (di['scanlabel'], di['sessionuid'], di['modality']))
            # Add to cache
            self.newscans += 1
        else:
            self.logger.debug('Unable to create session %s with uid %s on project %s' %
                              (di['sessionlabel'], di['sessionuid'], di['project']))
            return False

        self.checked_values['projects'][di['project']]['scanuids'][di['scanuid']] = di['scanlabel']
        self.checked_values['projects'][di['project']]['scanlabels'][di['scanlabel']] = di['scanuid']

        return True

    def iterate_dup(self, project, duptype, value):
        newname = value
        num = 0

        while newname in self.checked_values[project][duptype]:
            newname = "%s_%s" % (value, num)
            num += 1

        return value

    def bytes_format(self, number_of_bytes):
        # Formats byte to human readable text
        if number_of_bytes < 0:
            raise ValueError("number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return str(number_of_bytes) + ' ' + unit

    def pull_dicom_tags(self, path):
        td = pydicom.read_file(path)

        myproject = None
        mysubject = None

        try:
            if not (self.splitlabel is not None and td[self.splitlabel]) and not td[self.subjectlabel].value:
                self.logger.error('Subject Label @ %s empty for %s, skipping' % (self.subjectlabel, path))
                return None
            elif not td[self.sessionlabel].value:
                self.logger.error('Session Label @ %s empty for %s, skipping' % (self.sessionlabel, path))
                return None
            elif not td[self.scanlabel].value:
                self.logger.error('Scan Label @ %s empty for %s, skipping' % (self.scanlabel, path))
                return None
            elif not td[self.scanuid].value:
                self.logger.error('Scan UID @ %s empty for %s, skipping' % (self.scanuid, path))
                return None
            elif not td[self.sessionuid].value:
                self.logger.error('Session UID @ %s empty for %s, skipping' % (self.sessionuid, path))
                return None
        except TypeError as e:
            self.logger.error('File %s dicom read error, missing key, skipping: %s' % (path, e))
            return None
        except LookupError as e:
            self.logger.error('File %s dicom read error, invalid encoding, skipping: %s' % (path, e))
            return None

        if self.splitlabel:
            try:
                if td[self.splitlabel].value:
                    mysplabel = str(td[self.splitlabel].value)
                    if ":" in mysplabel:
                        # Check for :, split and use combo
                        (myproject, mysubject) = mysplabel.split(':')
                    else:
                        # If just a single string, check if that project exists
                        # If so, then use that project
                        if not self.check_project(mysplabel):
                            myproject = self.project
                        else:
                            myproject = mysplabel
                        # If single string, then use that as subject
                        mysubject = self.subject

                    # Check if project exists, if not do defaults
                    if not self.check_project(myproject):
                        myproject = self.project
                        mysubject = self.subject
                else:
                    myproject = self.project
                    mysubject = self.subject
            except Exception as e:
                # Default to defaults on error
                myproject = None
                mysubject = None

        if myproject is None and self.projectlabel is not None:
            myproject = td[self.projectlabel].value
            if not myproject:
                self.logger.error('Project label @ %s empty for %s, skipping' % (myproject, path))
                return None

        if myproject is None:
            myproject = self.project

        if mysubject is None and self.subjectlabel is not None:
            try:
                if td[self.subjectlabel].value:
                    mysubject = self.strip_invalid(td[self.subjectlabel].value)
                else:
                    mysubject = None
            except Exception as e:
                mysubject = None

        if mysubject is None:
            mysubject = self.project

        try:
            if td[self.sessiondate].value:
                year = td[self.scandate].value[0:4]
                month = td[self.scandate].value[5:6]
                day = td[self.scandate].value[7:8]
                sessiondate = "%s/%s/%s" % (month, day, year)
            else:
                sessiondate = None
        except Exception as e:
            sessiondate = None

        try:
            if td[self.studydesc].value:
                studydesc = td[self.studydesc].value
            else:
                studydesc = None
        except Exception as e:
            studydesc = None

        try:
            if td[self.seriesdesc].value:
                seriesdesc = td[self.seriesdesc].value
            else:
                seriesdesc = None
        except Exception as e:
            seriesdesc = None

        try:
            if td[self.scandate].value:
                year = td[self.scandate].value[0:4]
                month = td[self.scandate].value[5:6]
                day = td[self.scandate].value[7:8]
                scandate = "%s/%s/%s" % (month, day, year)
            else:
                scandate = None
        except Exception as e:
            scandate = None

        mydi = {
            'subjectlabel': self.strip_invalid(mysubject),
            'sessionlabel': self.strip_invalid(td[self.sessionlabel].value),
            'scanlabel': self.strip_invalid(td[self.scanlabel].value),
            'scanuid': td[self.scanuid].value,
            'sessionuid': td[self.sessionuid].value,
            'modality': self.translate_modality(td[self.modality].value),
            'project': self.strip_invalid(myproject),
            'path': path,
            'sessiondate': sessiondate,
            'scandate': scandate,
            'sessiondesc': studydesc,
            'scandesc': seriesdesc
        }

        if self.splitsample:
            print(json.dumps(mydi))
            exit(0)

        return mydi

    def update_map(self, di):
        if di['project'] not in self.sessionmap['projects']:
            self.sessionmap['projects'][di['project']] = {'subjects': dict()}
        if di['subjectlabel'] not in self.sessionmap['projects'][di['project']]['subjects']:
            self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']] = {'sessions': dict()}
        if di['sessionlabel'] not in self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions']:
            self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions'][di['sessionlabel']]\
                = list()
        self.sessionmap['projects'][di['project']]['subjects'][di['subjectlabel']]['sessions'][di['sessionlabel']].\
            append(di)

        return True

    def server_pull_headers(self):
        # Trigger final pull of remote headers via api for all sessions
        # 'http://my.xnat.org/REST/projects/MyProject/subjects/ThisSubject/experiments/ThisSession?pullDataFromHeaders=true'
        # Update stats for all sessions to refresh catalog
        # /services/refresh/catalog?resource=/archive/projects/PROJECT/subjects/SUBJECT/experiments/EXPT&options=populateStats
        self.renew_httpsession()

        for thisproject in self.sessionmap['projects']:
            for thissubject in self.sessionmap['projects'][thisproject]['subjects']:
                for thissession in self.sessionmap['projects'][thisproject]['subjects'][thissubject]['sessions']:
                    self.logger.info(
                        "Pulling headers from session %s [%s %s]" % (thissession, thisproject, thissubject))
                    response = self.httpsess.put(
                        self.host + '/REST/projects/%s/subjects/%s/experiments/%s?pullDataFromHeaders=true&'
                                    'event_reason=upload' % (thisproject, thissubject, thissession))

                    response = self.httpsess.post(
                        self.host + '/data/services/refresh/catalog?resource=/archive/projects/%s/subjects/%s'
                                    '/experiments/%s&options=populateStats&event_reason=upload' %
                        (thisproject, thissubject, thissession))

        return True

    def strip_invalid(self, mytext):
        mytext = str(mytext).replace(" ", "_")
        return re.sub(r'\W+', '_', mytext)

    def translate_modality(self, modality):
        # Translate modality code from files into xnat mapping
        if modality == 'MR':
            return 'mr'
        elif modality == 'PT':
            return 'pet'
        elif modality == 'CT':
            return 'ct'
        elif modality == 'XA':
            return 'xa'
        elif modality == 'US':
            return 'us'
        elif modality == 'RT':
            return 'rt'
        elif modality == 'CR':
            return 'cr'
        elif modality == 'OPT':
            return 'opt'
        elif modality == 'MG':
            return 'mg'
        elif modality == 'NM':
            return 'nm'
        elif modality == 'SR':
            return 'sr'
        elif modality == 'SC':
            return 'otherDicom'
        else:
            return 'otherDicom'

    def get_session_modality(self, project, subject, session):
        modalities = list()
        # Pulls session modality based on scans contained within
        for thisscan in self.sessionmap['projects'][project]['subjects'][subject]['sessions'][session]:
            modalities.append(thisscan['modality'])

        modalities = list(dict.fromkeys(modalities))

        if len(modalities) > 1 and 'sr' in modalities:
            modalities.remove('sr')

        if len(modalities) == 1:
            return modalities[0]
        elif 'pet' in modalities and 'mr' in modalities:
            return 'petmr'
        elif 'pet' in modalities and 'ct' in modalities:
            return 'pet'

        return modalities[0]

    def sessionmap_dump(self):
        # Dump filetree to output for debugging purposes
        self.logger.info('Dumping file tree map to file %s' % self.dumpmap)
        opts = jsbeautifier.default_options()
        opts.ident_size = 2
        f = open(self.dumpmap, "w")
        f.write(jsbeautifier.beautify(json.dumps(self.sessionmap), opts))
        return True

    def renew_httpsession(self):
        # Set up request session and get cookie
        if self.lastrenew is None or ((self.lastrenew + self.sessiontimeout) < datetime.datetime.now()):
            self.logger.debug('[SESSION] Renewing http session as %s from %s with timeout %d' % (self.username,
                                                                                                 self.host,
                                                                                                 self.timeout))
            # Renew expired session, or set up new session
            self.httpsess = requests.Session()

            # Retry logic
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.httpsess.mount('http://', adapter)
            self.httpsess.mount('https://', adapter)

            # Log in and generate xnat session
            response = self.httpsess.post(self.host + '/data/JSESSION', auth=(self.username, self.password),
                                          timeout=(30, self.timeout))
            if response.status_code != 200:
                self.logger.error("[SESSION] Renewal failed, no session acquired: %d %s" % (response.status_code,
                                                                                            response.reason))
                exit(1)

            self.lastrenew = datetime.datetime.now()
        else:
            # self.logger.debug('[SESSION] Reusing existing https session until %s' % (self.lastrenew +
            #                                                                         self.sessiontimeout))
            return True

        return True

    def close_httpsession(self):
        # Logs out of session for cleanup
        self.httpsess.delete(self.host + '/data/JSESSION', timeout=(30, self.timeout))
        self.logger.debug('[SESSION] Deleting https session')
        self.httpsess.close()
        return True
