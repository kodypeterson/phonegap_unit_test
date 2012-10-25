#!/usr/bin/python
import subprocess
import sys
import os
import urllib
import json
from optparse import OptionParser
import phonegap

parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory",
                  help="Your Phonegap www directory source")
                  
parser.add_option("--skip-js", dest="skipjslint",
                  help="Skip jsLint phase", action="store_true")
                  
parser.add_option("--skip-html", dest="skiphtmllint",
                  help="Skip htmlLint phase", action="store_true")
                  
parser.add_option("--build", dest="build",
                  help="Skip htmlLint phase", action="store_true")

(options, args) = parser.parse_args()

#REQUIRE -D
if options.directory is None:
    print "ERROR: You must specify a directory.\nSee -h for more info"
    sys.exit()
    
skipFileList = []
jsFileList = []
htmlFileList = []
rootdir = options.directory

accelerometer = []


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

for root, subFolders, files in os.walk(rootdir):
    for file in files:
        if ".js" in file:
            #GET ALL JS FILES
            jsFileList.append(os.path.join(root,file))
        elif ".html" in file:
            #GET ALL HTML FILES
            htmlFileList.append(os.path.join(root,file))
        elif ".htm" in file:
            #GET ALL HTM FILES
            htmlFileList.append(os.path.join(root,file))
            
#READ .IGNORE FILE
try:
    with open(rootdir+"/.ignore") as f:
        for line in f:
            skipFileList.append(rootdir+line)
except IOError as e:
    nothing

print "***********************************************"
print "*  WELCOME TO THE PHONEGAP UNIT TEST & BUILD  *"
print "*             UNOFFICIAL PROCESS              *"
print "*                                             *"
print "*           BUILT BY: HEADWEBMONKEY           *"
print "* github.com/headwebmonkey/phonegap_unit_test *"
print "***********************************************"

#JS LINT
if options.skipjslint is True:
    print "PHASE 1: jsLint Tests - " + OKBLUE + "SKIPPED" + ENDC
else:
    #START NEW PHASE
    print "PHASE 1: jsLint Tests\n"

    #RUN JSLINT
    for file in jsFileList:
        print "\t"+file+": ",
        if any(file in s for s in skipFileList):
            print OKBLUE + "SKIPPED" + ENDC
        else:
            p = subprocess.Popen('./jslint '+file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
            good = True
            for line in p.stdout.readlines():
                if not "jslint: No problems found in" in line:
                        print FAIL + "FAILED" + ENDC + "\n\t\t"+line
                        sys.exit()
                else:
                        print OKGREEN + "PASSED" + ENDC
            retval = p.wait()

#HTML LINT
if options.skiphtmllint is True:
    print "\nPHASE 2: htmlLint Tests - " + OKBLUE + "SKIPPED" + ENDC
else:
    #START NEW PHASE
    if options.skipjslint is True:
    	print "PHASE 2: htmlLint Tests\n"
    else:
    	print "\n\nPHASE 2: htmlLint Tests\n"

    #RUN HTML-LINT
    for file in htmlFileList:
        print "\t"+file+": ",

        if any(file in s for s in skipFileList):
            print OKBLUE + "SKIPPED" + ENDC
        else:
            params = {}
    
            params['output'] = "json"
            params['type'] = "text/html"
            params['doctype'] = "HTML 4.01 Transitional"
            with open(file, 'r') as content_file:
                params['uploaded_file'] = content_file.read()

            params = urllib.urlencode(params)
            f = urllib.urlopen("http://validator.w3.org/check", params)
            json_return = f.read()
            if json_return == "Rate limit exceeded":
                print "RATE LIMIT EXCEEDED!!!"
                sys.exit()
            else:
                json_return = json.loads(json_return)
                if len(json_return['messages']) > 0:
                    print FAIL + "FAILED" + ENDC
                    for message in json_return['messages']:
                        print "\t\tLine: "+str(message['lastLine'])+":"+str(message['lastColumn'])+" - "+str(message['message'])
                    sys.exit()
                else:
                    print OKGREEN + "PASSED" + ENDC

#PHONEGAP TEST
#START NEW PHASE
if options.skiphtmllint is True:
    print "\nPHASE 3: phonegapLint Tests\n"
else:
    print "\n\nPHASE 3: phonegapLint Tests\n"
#ACCELEROMETER
filesToTest = jsFileList + htmlFileList
for file in filesToTest:
    if any(file in s for s in skipFileList):
        continue
    else:
    	print "\t"+file
        with open(file, 'r') as content_file:
            contents = content_file.read()
            if "navigator.accelerometer" in contents:
            	print "\t\tAccelerometer:",
                phonegap.testAccelerometer(contents)
            else:
            	print "\t\tAccelerometer: " + OKBLUE + "NOT FOUND" + ENDC
            if "navigator.camera" in contents:
                print "\t\t       Camera:",
            	phonegap.testCamera(contents)
            else:
            	print "\t\t       Camera: " + OKBLUE + "NOT FOUND" + ENDC
		
#RUN PHONEGAP-LINT

print "\n\nTEST COMPLETE!"