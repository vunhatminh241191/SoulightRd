import sys, shutil, os

PROJECT_PATH = "soulightrd"

def setupConfig(stage): 
	common = PROJECT_PATH + "/config/common.py"
    	shutil.copy(common,PROJECT_PATH + "/settings.py")
	stage_file = open(PROJECT_PATH + "/config/" + stage + ".py","r")
	dest_file = open(PROJECT_PATH + "/settings.py","a+")
	dest_file.write("\n\n\n")
	for line in stage_file:
		dest_file.write(line)

def main():
    print "...RUNNING SETUP CONFIGURATION..."
    try:
        stage = sys.argv[1]
        setupConfig(stage)
        print "Setup configuration successfully"
    except Exception:
        print "Setup configuration error"
        raise

if __name__ == "__main__":
    main() 
