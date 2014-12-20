import os, sys, string, random, tempfile
from datetime import datetime

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization, Project, Photo
from soulightrd.apps.main.models import OrganizationBoardMember
from soulightrd.apps.main.models import ProjectBoardMember
from soulightrd.apps.app_helper import generate_unique_id

from django.contrib.auth.models import User
from django import db
from django.core import files

image_path = os.path.dirname(SETTING_PATH + '/assets/media/upload_storage/photo/images/')

def create_photo_object(target_object, user):
	# random year
	year = random.choice(range(2005, 2014))
	month = random.choice(range(1, 12))
	day = random.choice(range(1, 28))

	each_image_path = os.path.join(image_path, random.choice(os.listdir(image_path)))

	with open(each_image_path) as f:
		data = f.read()

	# get image file
	image_file = tempfile.NamedTemporaryFile(delete=False)
	image_file.write(data)
	image_file.name = os.path.basename(each_image_path)

	photo = Photo.objects.create(
		unique_id=generate_unique_id("photo"),
		caption="abcd",
		image= files.File(image_file),
		upload_date = datetime(year,month,day),
		user_post = user,
		object_unique_id = target_object.unique_id)
	photo.save()
	return photo

def main(): 
	print "... RUNNING GENERATE PHOTO SCRIPT "
	photo = Photo.objects.all()

	if len(Photo.objects.filter(object_unique_id=None)) < 10:
		try:
			organizations = Organization.objects.all()
			projects = Project.objects.all()

			for organization in organizations:
				for i in xrange(2):
					user = OrganizationBoardMember.objects.filter(
						organization=organization)[0].user
					photo = create_photo_object(organization, user)

					organization.images.add(photo)
					organization.save()

			for project in projects:
				for i in xrange(2):
					user = ProjectBoardMember.objects.filter(
						project=project)[0].user
					photo = create_photo_object(project, user)

					project.images.add(photo)
					project.save()

			print "Generate Photo Successfully"
			db.close_connection()
		except:
			print "Generate Photo Failed"
			raise
		db.close_connection()
	else:
		print "Photo dummy data already created"

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()