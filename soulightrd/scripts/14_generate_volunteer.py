import os, sys,random
from datetime import datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from soulightrd.apps.main.models import Project, Volunteer
from dummy_database import PROJECT_TESTING, NAMES

def main():
	print "... RUNNING GENERATE VOLUNTEER SCRIPT ..."

	try:
		for i in xrange(len(PROJECT_TESTING)):

			year = random.choice(range(2005, 2014))
			month = random.choice(range(1, 12))
			day = random.choice(range(1, 28))

			volunteer = Volunteer.objects.create(
				user=User.objects.get(username=NAMES[random.randint(54,len(NAMES)-1)].lower()),
				project=Project.objects.get(unique_id=PROJECT_TESTING[i]),
				is_signed_confirmation=True, register_date = datetime(year,month,day))

			volunteer.save()
		print "Generate Volunteer Successfully"
	except:
		print "Generate Volunteer Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()