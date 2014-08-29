import sys, os

STAGE_NAME = {"dev":None, "prod": None}

if len(sys.argv) < 2 or sys.argv[1] not in STAGE_NAME:
	valid_stage = str(STAGE_NAME.keys()).replace("[","").replace("]","")
	print "Usage: python " + __file__ + " argv[1]" 
	print "argv[1] can be one of the following: " + valid_stage
	sys.exit()

CATALOGUE = "CATALOGUE"
COMMENT_CHARACTER = "<!--"

PROJECT_ROOT = os.path.dirname(__file__)
PROJECT_NAME = "soulightrd"
PROJECT_SCRIPT = "scripts"
PROJECT_PATH = os.path.join(PROJECT_ROOT, PROJECT_NAME, PROJECT_SCRIPT)

CATALOGUE_PATH = os.path.join(PROJECT_PATH,CATALOGUE)


argument = " ".join(sys.argv)

list_file = []
f = open(CATALOGUE_PATH,"r")
for filename in f:
    if len(filename.replace("\n","")) != 0 and filename.startswith(COMMENT_CHARACTER) == False:
        list_file.append(filename.replace("\n",""))

for script in list_file:
	cmd = "python " + PROJECT_PATH + "/" + script + argument[argument.find(" "):]
	os.system(cmd)

