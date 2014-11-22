import os, sys, string, random
from datetime import datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization
from soulightrd.apps.app_helper import get_any_admin_object, generate_unique_id

from dummy_database import NAMES, ORGANIZATION_NAMES, PHONE_TESTING

from django.contrib.auth.models import User, Permission
from cities_light.models import City, Country
from django import db

edit_organization_permission = Permission.objects.get(codename='change_organization')

def main():
	print "... RUNNING GENERATE ORGANIZATION SCRIPT ..."
	organizations = Organization.objects.all()
	k=0
	if len(organizations) == 0:
		try:
			for i in xrange(len(ORGANIZATION_NAMES)):
				# random date
				year = random.choice(range(2005, 2014))
				month = random.choice(range(1, 12))
				day = random.choice(range(1, 28))

				organization = Organization.objects.create(
					unique_id=generate_unique_id("organization"), 
					created_by=User.objects.get(username=NAMES[k].lower()),
					name="Organization " + str(i),
					description="abcde",
					phone='+' + PHONE_TESTING[i], 
					email= ORGANIZATION_NAMES[i] + '@gmail.com',
					address="111 Le Thanh Ton, District 1",
					city=City.objects.order_by('?')[0],
					submit_date=datetime(year,month,day))
				organization.normal_member.add(User.objects.get(username=NAMES[k+1].lower()))
				organization.save()

				i += 1
				k += 2
			print "Generate Organization Successfully"
		except:
			print "Generate Organization Failed"
			raise
		db.close_connection()
	else:
		print "Organization dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()