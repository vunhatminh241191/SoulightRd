import os, sys,random

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Donation, Project
from dummy_database import NAMES, PROJECT_TESTING
from django.contrib.auth.models import User

def main():
	print "... RUNNING GENERATE DONATION ..."

	try:
		for i in xrange(len(NAMES)):
			testing_project = PROJECT_TESTING[random.randint(0,len(PROJECT_TESTING))]
			donation = Donation.objects.create(
				user = User.objects.get(username=NAMES[random.randint(0,len(NAMES))].lower()),
				project = Project.objects.get(unique_id=testing_project),
				amount = random.randint[1,200])
			donation.save()
		print "Generate Donation Successfully"
	except:
		print "Generate Donation Failed"
		raise

if __name__ == '__main__':
	stag = sys.argv[1]
	if stag != "prod":
		main()