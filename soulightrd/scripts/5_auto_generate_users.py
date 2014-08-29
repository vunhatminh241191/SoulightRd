import os, sys

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User

from frittie.apps.main.models import Photo
from frittie.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID
from frittie.apps.app_helper import get_any_admin_object, generate_unique_id


names = ["Smith","Anderson","Clark","Wright","Mitchell","Johnson","Thomas","Rodriguez","Lopez","Perez","Williams","Jackson","Lewis","Hill","Roberts","Jones","White","Lee","Scott","Turner","Brown","Harris","Walker","Green","Phillips","Davis","Martin","Hall","Adams","Campbell","Miller","Thompson","Allen","Baker","Parker","Wilson","Garcia","Young","Gonzalez","Evans","Moore","Martinez","Hernandez","Nelson","Edwards","Taylor","Robinson","King","Carter","Collin"]

def main():
	print "...RUNNING GENERATE USERS SCRIPT..."
	try:
		admin = get_any_admin_object()
		avatar = None
		try:
			avatar = Photo.objects.get(unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_male_icon'])
		except Photo.DoesNotExist:
			avatar = Photo.objects.create(caption="default_male_icon",user_post=admin,image=DEFAULT_IMAGE_PATH_MAPPING['default_male_icon'],unique_id=generate_unique_id("photo"))

		cover_picture = None
		try:
			cover_picture = Photo.objects.get(unique_id=DEFAULT_IMAGE_UNIQUE_ID['default_cover_picture'])
		except Photo.DoesNotExist:
			cover_picture = Photo.objects.create(caption="default_male_icon",user_post=admin,image=DEFAULT_IMAGE_PATH_MAPPING['default_cover_picture'],unique_id=generate_unique_id("photo"))
		i = 0
		for name in names:
			i = i + 1 
			test_email = "test"+str(i)+"@frittie.com"
			user = User.objects.create_user(name.lower(),test_email, 'frittie4success')
			user.first_name = name 
			user.save()
			user.get_profile().avatar = avatar
			user.get_profile().cover_picture = cover_picture
			user.get_profile().save()
		print "Generate users successfully"
	except:
		print "Generate User Failed"
		raise

if __name__ == "__main__":
	stage = sys.argv[1]
	if stage != "prod" and len(User.objects.filter(email='test1@frittie.com')) == 0: 
		main()
