import os, sys, random, string, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User

from soulightrd.apps.main.models import Project, Organization, Photo, City
from dummy_database import PROJECT_TESTING, ORGANIZATION_NAMES, NAMES
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id

def main():
	print "... RUNNING GENERATE PROJECT SCRIPT ..."

	admin = get_any_admin_object()
	try:
		project_picture = Photo.objects.get(
			unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_picture'])
	except Photo.DoesNotExist:
		project_picture = Photo.objects.create(caption="default_project_picture"
			,user_post=admin,image=DEFAULT_IMAGE_PATH_MAPPING['default_project_picture']
			,unique_id=generate_unique_id("photo"))	

	try:
		for i in xrange(len(ORGANIZATION_NAMES)):
			organization = Organization.objects.get(unique_id=ORGANIZATION_NAMES[i])
			for k in xrange(3):
				project = Project.objects.create(unique_id=PROJECT_TESTING[k],
					description='abcde', project_type=random.choice(string.ascii_lowercase),
					funding_goal=random.randint(1,100), current_funding=random.randint(1,100),
					project_image=project_picture,organization=organization, 
					project_duration=random.randint(1,12), 
					project_start_date=datetime.datetime.today(),
					project_location=City.objects.get(id=random.randint(1,23292)))
				project.followers.add(User.objects.get(username=NAMES[random.randint(1,len(NAMES))]))
				project.save()
		print "Generate Project Successfully"
	except:
		print "Generate Project Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()