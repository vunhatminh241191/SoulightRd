import os, sys, uuid

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(PROJECT_PATH)
sys.path.append(SETTING_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Photo
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id
from django import db

def main():
	try:
		print "...GENERATE DEFAULT IMAGE..."
		for key,value in DEFAULT_IMAGE_UNIQUE_ID.iteritems():
			try:
				photo = Photo.objects.get(unique_id=value)
			except Photo.DoesNotExist:
				admin = get_any_admin_object()
				try:
					new_photo = Photo.objects.create(caption=key,user_post=admin,
						unique_id=value,image=DEFAULT_IMAGE_PATH_MAPPING[key],photo_type='default_image')
					new_photo.save()
				except:
					raise
		print "...Generate default image successfully..."
	except:
		print "Generate default image failed"
		raise
	db.close_connection()

if __name__ == "__main__":
	main()
