from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend as DjangoSmtpEmailBackend

from soulightrd.settings import MEDIA_URL, SERVER_EMAIL
from soulightrd.settings import MANDRILL_API_KEY, MAX_MANDRILL_EMAIL_ALLOW
from soulightrd.settings import EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS

from soulightrd.apps.main.constants import PROJECT_TYPE, GENDER, NEW, OLD
from soulightrd.apps.main.constants import PHOTO_TYPE, NOTIFICATION_STATUS, NOTIFICATION_TYPE
from soulightrd.apps.main.constants import MESSAGE_STATUS, COMMENT_TYPE, REPORT_TYPE
from soulightrd.apps.main.constants import PRIVACY_STATUS, PUBLIC

from allauth.socialaccount.models import SocialAccount

from phonenumber_field.modelfields import PhoneNumberField

import moneyed
from djmoney.models.fields import MoneyField

from cities_light.models import City

try:
	storage = settings.MULTI_IMAGES_FOLDER + '/'
except AttributeError:
	storage = 'upload_storage/'


class SocialFriendsManager(models.Manager):
    def assert_user_is_social_auth_user(self, user):
        if not isinstance(user, SocialAccount):
            raise TypeError("user must be UserSocialAuth instance, not %s" % user)

    def fetch_social_friends(self, social_auth_user):
        self.assert_user_is_social_auth_user(social_auth_user)
        friends_provider = FacebookFriendsProvider()
        friends = friends_provider.fetch_friends_data(social_auth_user)
        return friends

    def existing_social_friends(self, user_social_auth=None, friends=None):
        self.assert_user_is_social_auth_user(user_social_auth)
        if not friends:
            friends = self.fetch_social_friends(user_social_auth)
        # Convert comma sepearated string to the list
        if isinstance(friends, basestring):
            friends = eval(friends)
        return User.objects.filter(socialaccount__uid__in=friends).all()  


    def get_or_create_with_social_auth(self, social_auth):
        self.assert_user_is_social_auth_user(social_auth)
        try:
            social_friend_list = self.filter(user_social_auth=social_auth).get()
            friends = social_friend_list.friends
            if len(friends) == 0:
                social_friend_list.friends = self.fetch_social_friends(social_auth)
                social_friend_list.save()
        except:
            # if no record found, create a new one
            friends = self.fetch_social_friends(social_auth)
            social_friend_list = SocialFriendList()
            social_friend_list.friends = friends
            social_friend_list.user_social_auth = social_auth
            social_friend_list.save()
        return social_friend_list

    def get_or_create_with_social_auths(self, social_auths):
        social_friend_coll = []
        for sa in social_auths:
            social_friend = self.get_or_create_with_social_auth(sa)
            social_friend_coll.append(social_friend)
        return social_friend_coll


class SocialFriendList(models.Model):
    user_social_auth = models.OneToOneField(SocialAccount, related_name="social_account")
    friends = models.TextField(blank=True)
    objects = SocialFriendsManager()

    def __unicode__(self):
        return "%s on %s" % (self.user_social_auth.user.username, self.user_social_auth.provider)

    def existing_social_friends(self):
        return SocialFriendList.objects.existing_social_friends(self.user_social_auth, self.friends)


class EmailTracking(models.Model):
	to_emails = models.TextField()
	email_template = models.CharField(max_length=200)
	subject = models.CharField(max_length=350,blank=True)
	text_content = models.TextField(blank=True)
	context_data = models.TextField()
	status = models.CharField(max_length=50,default="pending")
	send_time = models.DateTimeField(blank=True,null=True)

	def is_reach_mandrill_limit(self):
		try:
			mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
			result = mandrill_client.users.info()
			last_month_sent = result['stats']['last_30_days']['sent']
			if last_month_sent >= MAX_MANDRILL_EMAIL_ALLOW:
				return True
		except Exception as e:
			logger.exception(e)
		return False

	def generate_email(self):
		context = ast.literal_eval(self.context_data)
		from_email = DEFAULT_SITE_NAME[0].upper() + DEFAULT_SITE_NAME[1:].lower() + " <" + DEFAULT_SERVER_EMAIL + ">"
		subject = render_to_string(EMAIL_SUBJECT_SNIPPET_TEMPLATE[self.email_template],context)
		text_content = render_to_string(EMAIL_CONTENT_TEXT_SNIPPET_TEMPLATE[self.email_template],context)
		html_content = render_to_string(EMAIL_CONTENT_HTML_SNIPPET_TEMPLATE[self.email_template],context)
		email = EmailMultiAlternatives(subject=subject,body=text_content,from_email=from_email,to=self.to_emails.split(","))
		email.attach_alternative(html_content, "text/html")
		email.content_subtype = "html"
		self.subject = subject
		self.text_content = text_content
		self.save()
		return email

	def send_email(self):
		is_reach_mandrill_limit = self.is_reach_mandrill_limit()
		try:
			email = self.generate_email()
			if is_reach_mandrill_limit:
				email.connection = DjangoSmtpEmailBackend(host="smtp.gmail.com",port=EMAIL_PORT,username=EMAIL_HOST_USER,password=EMAIL_HOST_PASSWORD,use_tls=EMAIL_USE_TLS)
				email.send()
				self.status = "success"
			else:
				email.send()
				response = email.mandrill_response[0]
				self.status = response['status']
			self.send_time = datetime.datetime.now()
			self.save()
		except Exception as e:
			logger.exception(e)
			self.status = "fail"
			self.save()

class Photo(models.Model):
	unique_id = models.CharField(max_length=100)
	caption = models.TextField(blank=True)
	image = models.ImageField(upload_to=storage+"/photo/%Y/%m/%d")
	upload_date = models.DateTimeField(auto_now_add=True)
	user_post = models.ForeignKey(User)
	photo_type = models.CharField(max_length=50,choices=PHOTO_TYPE,blank=True)
	object_unique_id = models.CharField(max_length=100,blank=True)

	def __unicode__(self):
		return self.image.name

class Notification(models.Model):
	unique_id = models.CharField(max_length=100)
	content = models.TextField()
	status = models.CharField(max_length=1,choices=NOTIFICATION_STATUS,default=NEW)
	notification_type = models.CharField(max_length=30,choices=NOTIFICATION_TYPE,null=True)
	notify_to = models.ManyToManyField(User, related_name='notify_to',blank=True,null=True)
	notify_from = models.ForeignKey(User, related_name='notify_from')
	date = models.DateTimeField(auto_now_add=True)
	
	def get_elapse_time(self):
		return get_elapse_time_text(self.date)


class Message(models.Model):
	unique_id = models.CharField(max_length=100)
	user_send = models.ForeignKey(User,related_name="user_send")
	user_receive = models.ForeignKey(User,related_name="user_receive")
	content = models.TextField()
	status = models.CharField(max_length=1,choices=MESSAGE_STATUS,default=NEW)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content

	def get_elapse_time(self):
		return get_elapse_time_text(self.date)


class Conversation(models.Model):
	unique_id = models.CharField(max_length=100)
	user1 = models.ForeignKey(User,related_name="user1")
	user2 = models.ForeignKey(User,related_name="user2")
	messages = models.ManyToManyField(Message,related_name="messages",null=True)
	latest_message = models.ForeignKey(Message,related_name="latest_message",null=True)


class Comment(models.Model):
	unique_id = models.CharField(max_length=100)
	comment_type = models.CharField(max_length=20,choices=COMMENT_TYPE)
	user = models.ForeignKey(User)
	content = models.TextField()
	create_date = models.DateTimeField(auto_now_add=True)
	edit_date =  models.DateTimeField(blank=True,null=True)
	reports = models.ManyToManyField("Report",related_name="comment_reports",blank=True,null=True)

	def get_create_elapse_time(self):
		return get_elapse_time_text(self.create_date)
	
	def get_edit_elapse_time(self):
		if self.edit_date != None:
			return get_elapse_time_text(self.edit_date)
		return None 


class Report(models.Model):
	unique_id = models.CharField(max_length=100)
	report_type = models.CharField(max_length=20,choices=REPORT_TYPE)
	user_report = models.ForeignKey(User,related_name='user_report',blank=True)
	date = models.DateTimeField(auto_now_add=True)
	report_content = models.TextField()

class OrganizationBoardMember(models.Model):
	user = models.ForeignKey(User,related_name='board_member_user')
	organization = models.ForeignKey("Organization",related_name='board_member_organization')
	role = models.CharField(max_length=100)

class Organization(models.Model):
	unique_id = models.CharField(max_length=100)
	name = models.CharField(max_length=300)
	description = models.TextField()
	website = models.URLField(blank=True,null=True)
	email = models.EmailField()
	phone = PhoneNumberField()
	address = models.CharField(max_length=300)
	normal_member = models.ManyToManyField(User,related_name='organization_normal_member',blank=True,null=True)
	is_verified = models.BooleanField(default=False)

	def get_board_members(self):
		return OrganizationBoardMember.objects.filter(organization=self)


class Project(models.Model):
	unique_id = models.CharField(max_length=100)
	title = models.CharField(max_length=300)
	description = models.TextField()
	project_image = models.ForeignKey(Photo,related_name="main_image")
	organization = models.ForeignKey(Organization,related_name='project_organization')
	project_type = models.CharField(max_length=1,choices=PROJECT_TYPE)
	funding_goal = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	current_funding = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	volunteer_goal = models.IntegerField(blank=True,null=True)
	current_volunteer = models.IntegerField(blank=True,null=True)
	project_duration = models.IntegerField(blank=True)
	project_start_date = models.DateTimeField()
	project_end_date = models.DateTimeField(blank=True,null=True)
	project_location = models.ForeignKey(City,related_name='project_location')
	comments = models.ManyToManyField(Comment, related_name='project_comments',blank=True,null=True)
	followers = models.ManyToManyField(User, related_name='project_followers',blank=True,null=True)

class ProjectActivity(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	responsible_member = models.ForeignKey(User,related_name='project_activity_responsible_member')
	image_proof = models.ManyToManyField(Photo,related_name='project_activity_image_proof',blank=True,null=True)
	date = models.DateTimeField()

class Payment(models.Model):
	user = models.ForeignKey(User,related_name='payment_user')
	amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	transaction_date = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True,related_name='profile')   
	basic_info = models.TextField(blank=True)
	gender = models.CharField(max_length=1,choices=GENDER,default="m")
	avatar = models.ForeignKey("Photo",blank=True,null=True,related_name="avatar")
	cover_picture = models.ForeignKey("Photo",blank=True,null=True,related_name='cover_picture')
	privacy_status = models.CharField(max_length=1,choices=PRIVACY_STATUS,default=PUBLIC)
	birthday = models.DateField(blank=True,null=True)
	facebook_id = models.CharField(max_length=40,blank=True,null=True)
	reports = models.ManyToManyField(Report,related_name='user_reports',blank=True,null=True)
	following_projects = models.ManyToManyField(Project,related_name='user_following_projects',blank=True,null=True)
	is_organization_board_member = models.BooleanField(default=False)
	address = models.CharField(max_length=300,blank=True)
	phone = PhoneNumberField(blank=True)


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



