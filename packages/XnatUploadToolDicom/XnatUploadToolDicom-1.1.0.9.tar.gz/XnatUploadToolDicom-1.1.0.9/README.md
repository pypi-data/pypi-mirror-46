
#Xnat dicom upload tool
Takes a single directory and uploads to dicom files to the xnat imaging informatics software platform.

##Summary
* Designed to upload a directory of dicom files to a single subject within a project
* Traverses filesystem tree, pulling tags from dicom files, and organizing them based on headers
* Batch uploads based on headers

## Use
usage: xnat-uploader-dicom [-h] [-c CONFIG] [--username USERNAME]
                           [--password PASSWORD] [--logfile LOGFILE] [-v]
                           [-t TIMEOUT] [-s SESSIONTIMEOUT] [-j JOBS] --host
                           HOST --project PROJECT
                           [--projectlabel PROJECTLABEL]
                           [--subjectlabel SUBJECTLABEL]
                           [--sessionlabel SESSIONLABEL]
                           [--scanlabel SCANLABEL] [--sessiondate SESSIONDATE]
                           [--scandate SCANDATE] [--deletesessions]
                           target
                         
                         
Arguments can either be passed in via the cli, or via config file (~/.xnatupload.cnf, or xnatupload.cnf in the
current working directory.) Arguments in the config file should match key/value pairs as in the cli. Example:

    host = http://localhost:8080
    username = myusername
    password = mypassword
    project = project1
    subject = subject1
    jobs = 4
    tmpdir = /tmp  
                          