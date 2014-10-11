import os, sys

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization, OrganizationBoardMember, Project
from dummy_database import NAMES, ORGANIZATION_NAMES
from django.contrib.auth.models import User

def main():
	print "... RUNNING GENERATE ORGANIZATION BOARD MEMBER SCRIPT ..."

	k = 26
	try:
		for i in xrange(len(ORGANIZATION_NAMES)):
			organizationboardmember = OrganizationBoardMember.objects.create(
				user = User.objects.get(username=NAMES[k].lower()),
				organization = Organization.objects.get(unique_id=ORGANIZATION_NAMES[i]))
			for project in Project.objects.filter(
				organization=Organization.objects.get(unique_id=ORGANIZATION_NAMES[i])):
				organizationboardmember.projects.add(project)
			organizationboardmember.save()
			k += 1
		print "Generate Organization Board Member Successfully"
	except:
		print "Generate Organization Board Member Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()