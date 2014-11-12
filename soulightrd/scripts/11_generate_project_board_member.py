import os, sys, random

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

from soulightrd.apps.main.models import ProjectBoardMember, Project

from dummy_database import NAMES

def main():
	print "... RUNNING GENERATE PROJECT BOARD MEMBER ..."
	project_board_member = ProjectBoardMember.objects.all()
	if len(project_board_member) == 0:
		try:
			projects = Project.objects.all()
			for project in projects:
				user = User.objects.get(username=NAMES[random.randint(81, 133)].lower())
				project_board_member = ProjectBoardMember.objects.create(user=user,
					project=project)
				project_board_member.save()
			print "Generate Project Board Member Successfully"
		except:
			print "Generate Project Board Member Failed"
			raise
		db.close_connection()
	else:
		print "Project Board Member dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()