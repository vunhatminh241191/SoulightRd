import os, sys, random, string
from datetime import datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

from soulightrd.apps.main.models import Project, Organization, Photo
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id

from dummy_database import PROJECT_TESTING, ORGANIZATION_NAMES, NAMES

from cities_light.models import City

def main():
	print "... RUNNING GENERATE PROJECT SCRIPT ..."
	
	k = 52
	projects = Project.objects.all()
	if len(projects) == 0:
		admin = get_any_admin_object()
		project_picture = None
		try:
			project_picture = Photo.objects.get(
				unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_picture'])
		except Photo.DoesNotExist:
			project_picture = Photo.objects.create(caption="default_project_picture"
				,user_post=admin,image=DEFAULT_IMAGE_PATH_MAPPING['default_project_picture']
				,unique_id=generate_unique_id("photo"))	
		
		try:
			organizations = Organization.objects.all()
			for organization in organizations:
				for i in range(1,3):
					year = random.choice(range(2005, 2014))
					month = random.choice(range(1, 12))
					day = random.choice(range(1, 28))

					project = Project.objects.create(unique_id=generate_unique_id("project"),
						title=organization.name + " Project " + str(i),
						description='abcde', project_type=random.choice(string.ascii_lowercase),
						funding_goal=random.randint(1,100), current_funding=random.randint(1,100),
						project_image=project_picture, project_duration=random.randint(1,12),
						organization=organization, 			 
						project_start_date=datetime(year, month, day),
						project_location=City.objects.order_by('?')[0])
					project.followers.add(User.objects.get(
						username=NAMES[k].lower()))
					project.save()

					organization.projects.add(project)
					organization.save()

					k += 1
			print "Generate Project Successfully"
		except:
			print "Generate Project Failed"
			raise
		db.close_connection()
	else:
		print "Project dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()