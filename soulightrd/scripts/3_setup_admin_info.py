import sys,os

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

ADMIN_FIRSTNAME = "Admin"
ADMIN_LASTNAME = "Dang Nguyen"
ADMIN_USERNAME = "dtn1712"
ADMIN_PASSWORD = "123456"
ADMIN_EMAIL = "dangnguyen_1712@yahoo.com"

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User

from frittie.apps.main.models import UserProfile, Photo
from frittie.apps.app_settings import DEFAULT_IMAGE_UNIQUE_ID

from django import db  
      

def main():
	print "...SETUP ADMIN INFO..."
	try:
		try:
			admin = User.objects.get(email=ADMIN_EMAIL)
		except:
			admin = User.objects.create(username=ADMIN_USERNAME)
			admin.set_password(ADMIN_PASSWORD)

		admin.is_staff = True
		admin.is_superuser = True
		admin.first_name = ADMIN_FIRSTNAME
		admin.last_name = ADMIN_LASTNAME
		admin.email = ADMIN_EMAIL
		admin.save()

		user_profile = None
		try:
			user_profile = UserProfile.objects.get(user__email=admin.email)
		except:
			user_profile = UserProfile.objects.create(user=admin)

		user_profile.avatar = Photo.objects.get(unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_male_icon'])
		user_profile.save()

		print "Setup Admin Info Successfully"
	except:
		stage = sys.argv[1]
		if stage == "prod":
			print "Seem like the environment is " \
					"not correct. Note that this script supposed to " \
					"work in the server environment for prod stage (e.g Heroku) " \
					"Please double check and try again"
		else:
			raise
	db.close_connection()
		
if __name__ == "__main__":
    main() 
