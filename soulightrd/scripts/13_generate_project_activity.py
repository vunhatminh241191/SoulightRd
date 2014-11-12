import os, sys,random, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User

from soulightrd.apps.main.models import ProjectActivity, Project, Photo, OrganizationBoardMember
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID

from dummy_database import NAMES

from django import db

def main():
	print "... RUNNING GENERATE PROJECT ACTIVITY ..."

	project_activities = ProjectActivity.objects.all()
	if len(project_activities) == 0:
		admin = get_any_admin_object()
		project_activity_picture = None
		try:
			project_activity_picture = Photo.objects.get(
				unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_activity_picture'])
		except Photo.DoesNotExist:
			project_activity_picture = Photo.objects.create(caption="default_project_activity_picture"
				,user_post=admin,image=DEFAULT_IMAGE_PATH_MAPPING['default_project_activity_picture']
				,unique_id=generate_unique_id("photo"))

		try:
			projects = Project.objects.all()
			for project in projects:

				year = random.choice(range(2005, 2014))
				month = random.choice(range(1, 12))
				day = random.choice(range(1, 28))

				responsible_member = None
				organization_board_members = OrganizationBoardMember.objects.all()
				for organization_board_member in organization_board_members:
					if project in organization_board_member.projects.all():
						responsible_member = organization_board_member.user
						break
						
				project_activity = ProjectActivity.objects.create(
					title='abcdef',
					project=project,
					description='done', 
					responsible_member=responsible_member,
					date=datetime.datetime(year,month,day))

				project_activity.image_proof.add(project_activity_picture)
				
				project_activity.save()
			print "Generate Project Activity Successfully"
		except:
			print "Generate Project Activity Failed"
			raise

		db.close_connection()
	else:
		print "Project Activity dummy data already created"


if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()