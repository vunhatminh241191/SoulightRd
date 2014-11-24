import os, sys,random

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Donation, Project

from dummy_database import NAMES, PROJECT_TESTING

from django.contrib.auth.models import User
from django import db

def main():
	print "... RUNNING GENERATE DONATION ..."
	donations = Donation.objects.all()
	if len(donations) == 0:
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
		db.close_connection()
	else:
		print "Donation dummy data already created"

if __name__ == '__main__':
	stag = sys.argv[1]
	if stag != "prod":
		main()