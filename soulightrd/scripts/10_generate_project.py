import os, sys, random, string, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Project, Organization, Photo, City
from dummy_database import PROJECT_TESTING, ORGANIZATION_NAMES
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID

def main():
	print "... RUNNING GENERATE PROJECT SCRIPT ..."

	project_picture = Photo.objects.get(unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_project_picture'])
	
	try:
		for i in xrange(len(ORGANIZATION_NAMES)-1):
			organization = Organization.objects.get(unique_id=ORGANIZATION_NAMES[i+1])
			for k in xrange(3):
				project = Project.objects.create(unique_id=PROJECT_TESTING[k], description='abcde', 
					project_type=random.choice(string.ascii_lowercase),
					funding_goal=random.randint(1,100), current_funding=random.randint(1,100),
					project_image=project_picture,organization=organization, 
					project_duration=random.randint(1,12), 
					project_start_date=datetime.datetime.today(),
					project_location=City.objects.get(id=random.randint(1,23292)))
				project.save()
		print "Generate Project Successfully"
	except:
		print "Generate Project Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()