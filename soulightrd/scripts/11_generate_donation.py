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
	Donation.objects.all().delete()
	try:
		for name in NAMES:
			user = User.objects.get(username=NAMES[random.randint(0,len(NAMES)-1)].lower())
			project = Project.objects.order_by('?')[0]
			donation = Donation.objects.create(user=user,project=project,amount=random.randint(1,100))
			donation.save()
		print "Generate Donation Successfully"
	except:
		print "Generate Donation Failed"
		raise

if __name__ == '__main__':
	stag = sys.argv[1]
	if stag != "prod":
		main()