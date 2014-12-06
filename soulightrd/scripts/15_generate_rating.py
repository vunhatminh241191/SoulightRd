import os, sys, random

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

from soulightrd.apps.main.models import Rating, Project, Organization
from soulightrd.apps.app_helper import generate_unique_id
from soulightrd.apps.main.constants import RATING_TYPE

def main():
	print "... RUNNING RATING SCRIPT ..."

	rating = Rating.objects.all()
	if len(rating) == 0:
		try:
			projects = Project.objects.all()
			for project in projects:
				rating = Rating.objects.create(
					unique_id=generate_unique_id("rating"),
					rating_type=RATING_TYPE[2][0],
					object_id=project.unique_id,
					rating=random.randint(1,5))
				rating.save()

			organizations = Organization.objects.all()
			for organization in organizations:
				rating = Rating.objects.create(
					unique_id=generate_unique_id("rating"),
					rating_type=RATING_TYPE[1][0],
					object_id=organization.unique_id,
					rating=random.randint(1,5))
				rating.save()

			print "Generate Rating Script Success"
		except:
			print "Generate Rating Script Fail"
			raise
		db.close_connection()
	else:
		print "Rating Script is generated"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != 'prod':
		main()