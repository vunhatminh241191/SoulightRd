import os, sys, string, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id

from dummy_database import NAMES, ORGANIZATION_NAMES, PHONE_TESTING

from django.contrib.auth.models import User
from django import db

string_integer = '1234567890'

def main():
	print "... RUNNING GENERATE ORGANIZATION SCRIPT ..."
	organizations = Organization.objects.all()
	if len(organizations) == 0:
		try:
			for i in xrange(len(ORGANIZATION_NAMES)):
				organization = Organization.objects.create(unique_id=generate_unique_id("organization")
					, phone='+' + PHONE_TESTING[i], email= ORGANIZATION_NAMES[i] + '@gmail.com')
				organization.normal_member.add(User.objects.get(username=NAMES[i].lower()))

				organization.save()
				i += 1
			print "Generate Organization Successfully"
		except:
			print "Generate Organization Failed"
			raise
		db.close_connection()
	else:
		print "Organization dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()