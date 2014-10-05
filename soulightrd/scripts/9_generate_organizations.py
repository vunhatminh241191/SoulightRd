import os, sys, string, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization
from dummy_database import NAMES, ORGANIZATION_NAMES, PHONE_TESTING
from django.contrib.auth.models import User

string_integer = '1234567890'

def main():
	print "... RUNNING GENERATE ORGANIZATION SCRIPT ..."

	try:
		for i in xrange(len(ORGANIZATION_NAMES)):
			organization = Organization.objects.create(unique_id=ORGANIZATION_NAMES[i]
				, phone='+' + PHONE_TESTING[i], email= ORGANIZATION_NAMES[i] + '@gmail.com')
			organization.normal_member.add(User.objects.get(username=NAMES[i].lower()))

			organization.save()
			i += 1
		print "Generate Organization successfully"
	except:
		print "Generate Organization Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()