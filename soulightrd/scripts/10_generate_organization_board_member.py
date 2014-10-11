import os, sys

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
	organization_board_members = OrganizationBoardMember.objects.all()
	if len(organization_board_members) == 0:
		try:
			organizations = Organization.objects.all()
			for organization in organizations:
				for name in NAMES:
					user = User.objects.get(username=name.lower())
					organization_board_member = OrganizationBoardMember.objects.create(user=user,organization=organization)
					projects = Project.objects.filter(organization=organization)
					for project in projects:
						organization_board_member.projects.add(project)
					organization_board_member.save()
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