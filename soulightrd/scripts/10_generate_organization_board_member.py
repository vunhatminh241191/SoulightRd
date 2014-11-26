import os, sys, random

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

from soulightrd.apps.main.models import Organization, OrganizationBoardMember, Project

from dummy_database import NAMES

def main():
	print "... RUNNING GENERATE ORGANIZATION BOARD MEMBER SCRIPT ..."

	k = 105
	organization_board_members = OrganizationBoardMember.objects.all()
	if len(organization_board_members) == 0:
		try:
			organizations = Organization.objects.all()
			for organization in organizations:
				user = User.objects.get(username=NAMES[k].lower())
				organization_board_member = OrganizationBoardMember.objects.create(
					user=user,organization=organization, role='tester 1')
				organization_board_member_1 = OrganizationBoardMember.objects.create(
					user=organization.created_by, organization=organization, role='tester 2')
				organization_board_member.save()
				organization_board_member_1.save()
				k += 1
			print "Generate Organization Board Member Successfully"
		except:
			print "Generate Organization Board Member Failed"
			raise
		db.close_connection()
	else:
		print "Organization Board Member dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()