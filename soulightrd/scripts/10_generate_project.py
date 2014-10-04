import os, sys, random, string

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Project, Organization, Photo
from dummy_database import PROJECT_TESTING, ORGANIZATION_NAMES
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID

def main():
	print "... RUNNING GENERATE PROJECT SCRIPT ..."

	project_picture = None
	try:
		project_picture = Photo.objects.get(unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_picture'])
	except Photo.DoesNotExist:
		project_picture = Photo.objects.create(caption="default_project_picture",user_post=admin,
			image=DEFAULT_IMAGE_PATH_MAPPING['default_project_picture'],unique_id=generate_unique_id("photo"))
	
	try:
		for i in xrange(len(ORGANIZATION_NAMES)):
			for k in xrange(3):
				project = Project.objects.create(unique_id=PROJECT_TESTING[k], description='abcde', 
					project_type=random.choice(string.ascii_lowercase),
					funding_goal=random.randint(1,100), current_funding=random.randint(1,100),
					)
				project.project_image.add(Photo.objects.get(
					unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_picture']))
				project.organization.add(Organization.objects.get(ORGANIZATION_NAMES[i]))
				project.save()
		print "Generate Project Successfully"
	except:
		print "Generate Project Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()