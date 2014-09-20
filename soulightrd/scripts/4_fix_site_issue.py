import sys,os

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

PROJECT_NAME = "soulightrd"
PROJECT_DOMAIN = "soulightrd.com"

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.sites.models import Site
from django import db

def main():
	print "...RUNNING FIX SITE ISSUE SCRIPT..."
	try:
		try:
			site = Site.objects.get(pk=1)
			site.domain = PROJECT_DOMAIN
			site.name = PROJECT_NAME
			site.save()
		except Site.DoesNotExist:
			Site.objects.create(domain=PROJECT_DOMAIN, name=PROJECT_NAME)

		print "Fix Site Issue Successfully"
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
