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
			organizationboardmember.add(
				Project.objects.get(organization=ORGANIZATION_NAMES[i]))
			organizationboardmember.save()
