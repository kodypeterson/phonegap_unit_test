import sys
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def testCamera(contents):
	methods = ["getPicture", "cleanup"]
	temp = contents.split("navigator.camera.")
	for t in temp:
	    testable = None
        for m in methods:
            if(t.startswith(m)):
                testable = m
	    if testable <> None:
	        if testable == "getPicture":
                    temp2 = t.split("(")
                    temp2 = temp2[1].split(",")
            	    if not "function "+temp2[0].strip(" ") in contents and temp2[0].strip(" ") <> "null":
            	    	failure("Success function \""+temp2[0].strip(" ")+"\" does not exist");
            	    if not "function "+temp2[1].strip(" ") in contents and temp2[1].strip(" ") <> "null":
            	    	failure("Failure function \""+temp2[1].strip(" ")+"\" does not exist");
	    else:
	    	temp2 = t.split(".")
	    	temp2 = temp2[0].split("(");
	        failure("No methods found that can handle \"" + temp2[0] + "\"!") 
	print OKGREEN + "PASSED" + ENDC
	
def testAccelerometer(contents):
	print "ACCELEROMETER"
	sys.exit()
	
def failure(error):
	print FAIL + "FAILURE" + ENDC
	print "\t\t\t\t" + FAIL + error + ENDC
	sys.exit()