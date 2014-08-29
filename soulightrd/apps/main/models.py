from django.db import models

# Create your models here.
class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True,related_name='profile')   
	basic_info = models.TextField(blank=True)
	gender = models.CharField(max_length=1,choices=GENDER,default="m")
	avatar = models.ForeignKey("Photo",blank=True,null=True,related_name="avatar")
	cover_picture = models.ForeignKey("Photo",blank=True,null=True,related_name='cover_picture')
	city = models.CharField(max_length=50,blank=True)
	state = models.CharField(max_length=2,choices=USA_STATES,blank=True)
	country = models.CharField(max_length=100,choices=DEFAULT_COUNTRIES_FORMAT,blank=True)
	privacy_status = models.CharField(max_length=1,choices=PRIVACY_STATUS,default=PUBLIC)
	birthday = models.DateField(blank=True,null=True)
	facebook_id = models.CharField(max_length=40,blank=True,null=True)
	reports = models.ManyToManyField(Report,related_name='user_reports',blank=True,null=True)

	def __unicode__(self):
		return unicode(self.user)

	def is_facebook_account(self):
		if self.facebook_id == None: return False
		if len(self.facebook_id) != 0:
			return True
		return False

	def get_user_fullname(self):
		first_name = self.user.first_name
		last_name = self.user.last_name
		if first_name.strip() == "" and last_name.strip() == "":
			username = self.user.username
			return username[0].upper() + username[1:].lower()
		return first_name + " " + last_name

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
		
post_save.connect(create_user_profile, sender=User)