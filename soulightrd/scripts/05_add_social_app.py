import sys,os

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_ROOT = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_PROVIDER, FACEBOOK_APP_NAME

from allauth.socialaccount.models import SocialApp

from django.contrib.sites.models import Site
from django import db

def main():
	print "...ADD FACEBOOK SOCIAL APP..."
	try:
		social_apps = SocialApp.objects.all()
		if len(social_apps) == 0:
			site = Site.objects.get(pk=1)
			facebook_app = SocialApp.objects.create(provider=FACEBOOK_PROVIDER,name=FACEBOOK_APP_NAME,client_id=FACEBOOK_APP_ID,secret=FACEBOOK_APP_SECRET)
			facebook_app.sites.add(site)
			facebook_app.save()
		print "Add facebook social app successfully"
	except Exception as exception:
		print "Add facebook social app failed"
		raise
	
	db.close_connection()
	
if __name__ == "__main__":
    main() 
