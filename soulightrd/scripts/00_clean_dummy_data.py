import os, sys, string, datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization, Project, OrganizationBoardMember
from soulightrd.apps.main.models import Donation, ProjectActivity, Volunteer

from django import db

def main():
	print "... RUNNING CLEANING DUMMY DATA SCRIPT ..."
	try:
		Organization.objects.all().delete()
		Project.objects.all().delete()
		OrganizationBoardMember.objects.all().delete()
		Donation.objects.all().delete()
		ProjectActivity.objects.all().delete()
		Volunteer.objects.all().delete()
		print "Clean Dummy Data Successfully"
	except:
		print "Clean Dummy Data Failed"
		raise

	db.close_connection()

if __name__ == '__main__':
	stage = sys.argv[1]
	if len(sys.argv) == 3 and stage == "dev" and sys.argv[2] == "--cleandummydata":
		main()