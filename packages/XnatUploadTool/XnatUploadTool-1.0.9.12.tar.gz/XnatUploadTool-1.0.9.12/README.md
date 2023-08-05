
#Xnat upload tool
Takes a single directory and uploads to xnat imaging informatics software platform.

##Summary
* Designed to upload a single session to a single subject within a project
* Can be used as a python module, or as a stand alone script
* Via the jobs argument, can be parallelized for maximum performance
* Handles login session rotation based on the 'sessiontimeout' setting, which should match your xnat server settings
* Recompresses data into zip file format to use high performance zip upload importer, can by bypassed by setting 'raw' mode.
* Performs validation on request, comparing dcm data and scan file counts in sessions to remote server post upload.
* Handles single file uploads of non-dicom data with custom headers

##Installation
Part of the PyPy repo, can be installed via either:

    pip install xnatuploadtool

or you prefer disutils:

    easy_install xnatuploadtool

Can also be installed directly by cloning this repo and running:

    python ./setup.py install

The executable script will be installed as 'xnat-uploader' in your system path. 

##Execution

Basic execution:

    xnat-uploader --host localhost:8080 --username myusername --password mypassword --project project1 
      --subject subject01 --session subject01_01 ./upload-data

Arguments can either be passed in via the cli, or via config file (~/.xnatupload.cnf, or xnatupload.cnf in the
current working directory.) Arguments in the config file should match key/value pairs as in the cli. Example:

    host = http://localhost:8080
    username = myusername
    password = mypassword
    project = project1
    subject = subject1
    jobs = 4
    tmpdir = /tmp

CLI example:

    usage: xnat-uploader [-h] [-c CONFIG] [--username USERNAME]
                         [--password PASSWORD] [--logfile LOGFILE]
                         [--tmpdir TMPDIR] [-V] [-r] [-v] [-t TIMEOUT]
                         [-s SESSIONTIMEOUT] [-j JOBS] [-d DATATYPE]
                         [--resource RESOURCE] --host HOST --project PROJECT
                         --subject SUBJECT [--subjectheaders SUBJECTHEADERS]
                         [--bsubjectheaders BSUBJECTHEADERS] [--session SESSION]
                         [--sessionheaders SESSIONHEADERS]
                         [--bsessionheaders BSESSIONHEADERS] [--scan SCAN]
                         [--scanheaders SCANHEADERS] [--bscanheaders BSCANHEADERS]
                         target
    
    Xnat upload script, takes a single directory and uploads to site. Target
    directory is a session, with any number of scans within it. Directories within
    are treated as scans, populated with either many separate dicom files or a
    single compressed flat archive of dicom files. Zip files found in the top
    level are treated as a scan and are expected to have a compressed archive of
    dcm files. The session name is assumed as the same as the zip file name,
    without the zip extension. If a single file is specifed rather than a
    directory, it is assumed to be non-dicom. This functionality requires the
    specification of other datatypes. This method is single threaded. Args that
    start with '--' (eg. --username) can also be set in a config file
    (~/.xnatupload.cnf or ./xnatupload.cnf or /etc/xnatupload.cnf or specified via
    -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for
    details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more
    than one place, then commandline values override config file values which
    override defaults.

    positional arguments:
      target                Target upload. Can be a directory with subdirectories
                            of dicom files, or a single non-dicom file
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Config file path
      --username USERNAME   Username, if not set will pull from XNATCREDS env
                            variable as USERNAME:PASSWORD
      --password PASSWORD   Password, if not set will pull from XNATCREDS env
                            variable as USERNAME:PASSWORD
      --logfile LOGFILE     File to log upload events to, if not set use stdout
      --tmpdir TMPDIR       Directory to untar/compress files to
      -V, --validate        Validate scan descriptions and filecounts after upload
      -r, --raw             Disable recompression as zip file uploading each scan
                            file individually. Severely impacts performance, but
                            can solve problems with extremely large sessions
      -v, --verbose         Produce verbose logging
      -t TIMEOUT, --timeout TIMEOUT
                            Read timeout in seconds, set to higher values if
                            uploads are failing due to timeout
      -s SESSIONTIMEOUT, --sessiontimeout SESSIONTIMEOUT
                            Session timeout for xnat site in minutes, to determine
                            session refresh frequency
      -j JOBS, --jobs JOBS  Run in X parallel processes to take advantage of
                            multiple cores
      -d DATATYPE, --datatype DATATYPE
                            Data type to upload
      --resource RESOURCE   Resource name for non-dicom files
      --host HOST           URL of xnat host
      --project PROJECT     Project to upload to
      --subject SUBJECT     Subject to upload to, can be string or in dicom tag
                            format (0000,0000). If tag in parenthesis is used,
                            will be pulled from first dicom file found.
      --subjectheaders SUBJECTHEADERS
                            Subject headers in json format
      --bsubjectheaders BSUBJECTHEADERS
                            Subject headers in base64 json format
      --session SESSION     Session name to use for upload, can be string or in
                            dicom tag format (0000,0000). If tag in parenthesis is
                            used, will be pulled from first dicom file found.
      --sessionheaders SESSIONHEADERS
                            Session headers in json format
      --bsessionheaders BSESSIONHEADERS
                            Session headers in base64 json format
      --scan SCAN           Scan to upload files to, can be string or in dicom tag
                            format (0000,0000)
      --scanheaders SCANHEADERS
                            Scan headers in json format
      --bscanheaders BSCANHEADERS
                            Scan headers in base64 json format
                        
##Filesystem Ingestion

When the tool is called with the -i flag, specifying a json config file, the tool will ingest the target filesystem. 
In this mode, filepaths and filenames will be matched against patterns to determine fields for the upload of said files. 
The format of this file must config to json standards. 

The following fields **must** be set through some mechanism: **subject, session, scan, xmlnamespace, datatype, resource**

Config keys:
 
  * '_defaults_': A dictionary of set static default values for various fields if no match is available.
  * '_match_': A regular expression which defines which files will be uploaded. Matches on entire filepath with name and extension.
  * '_exclude_': A regular expression of which files will be excluded. Matches on entire filepath with name and extension.
  * '_patterns_': A list of dictionaries that define how various fields are extracted from the filename/path
  
Patterns (applied in listed order):
 
   * '_type_': (required) Which field to extract using pattern. Subjectfield, sessionfield, and scanfield are standard 
   datatype specific fields. Subjectfield-custom, sessionfield-custom, and scanfield-custom are custom fields specific 
   to the datatype, and allow for extended info about the data being uploaded. Examples of these fields can be found at 
   https://wiki.xnat.org/docs16/4-developer-documentation/using-the-xnat-rest-api/xnat-rest-xml-path-shortcuts. 
   Multiple field types can be specified.
   * '_source_': (required) Can be set to filepath (path to file without filename), filename (full filename), filename-no-ext 
   (the filename with no .extension), or filename-ext (just the .extension)
   * '_split_': (optional) A list of settings for how to extract the field from the source. This can be up to three items: 
   The first is character to split the string on. The second is a list of field numbers (starting with 1) to extract. 
   The third, which is optional, is a character to rejoin the string on.
   * '_subsplit_': (optional)  In the same format as a split, this secondary split occurs after the filename path has 
   been split a first time. This allows for further splitting from resulting names.
   * '_range_': Range is list of numbers, expecting at least 1. The first specifies the first character in the output 
   to use, the second the last. If either is specified as negative, they are counted from the end of the string rather 
   than the start. Use cooresponds to python slice notation.
   * '_replace_': A list, first element is character to be replaced with character in second element.
   * '_modifiers_': A list of transforms to perform on the field after other processing is complete. This is a pass 
   through to python string operations.
   Example use: ['upper' (entire string is uppercase), 'capitalize' (first letter is capitalized)]
 
   * '_datefmt_': Converts a date string in the format of MMDDYYYY to usable date format for session and scan fields
   * '_adatefmt_': Converts a date string in the format of YYYYMMDD to usable date format for session and scan fields
 
Example:
 
     {
      "defaults": {
        "xmlnamespace": "xnat",
        "datatype": "cf",
        "resource": "bin"
      },
      {
      "match": "^.*.bin$",
      "exclude": "^.*header.*$",
      "patterns": [
        {
          "type": "subject",
          "source": "filepath",
          "split": ["/", [1]],
          "subsplit": ["-", [2]]
        },
        {
          "type": "session",
          "source": "filename",
          "split": ["_", [1]
        },
        {
          "type": "scan",
          "source": "filename-no-ext",
          "split": ["-", [7,8,9], "-"]
        },
        {
          "type": "sessionfield-custom",
          "fieldname": "date",
          "source": "filename",
          "split": ["-", [3, 4, 5]]
        },
        {
          "type": "sessionfield-custom",
          "fieldname": "modality",
          "source": "filename",
          "split": ["-", [1]],
          "modifiers": ["lower"]
        },
        {
          "type": "scanfield-custom",
          "fieldname": "laterality",
          "source": "filename",
          "split": ["-", [7]]
        },
        {
          "type": "scanfield-custom",
          "fieldname": "stereoscopy",
          "source": "filename-no-ext",
          "split": ["-", [8]]
        },
        {
          "type": "scanfield-custom",
          "fieldname": "test",
          "source": "filename-no-ext",
          "range": [2,-2]
        }
      ]
    } 
