from django.conf import settings
from django.core import files
from django.contrib.gis.geoip import GeoIP

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib import messages

from allauth.utils import generate_unique_username
from allauth.utils import (import_attribute,
					 email_address_exists,
					 valid_email_or_none)


from allauth.account.utils import user_username, user_email, user_field, get_user_model
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.models import EmailAddress

from allauth.account import app_settings as account_settings
from allauth.account.app_settings import EmailVerificationMethod

from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from soulightrd.apps.app_helper import generate_unique_id, get_client_ip
from soulightrd.apps.main.models import Photo, SocialFriendList
from soulightrd.apps.main.constants import GENDER_MAP_BY_NAME, DEFAULT_SERVER_EMAIL, DEFAULT_SITE_NAME
from soulightrd.apps.app_settings import DEFAULT_IMAGE_PATH_MAPPING, DEFAULT_IMAGE_UNIQUE_ID
from soulightrd.settings import MEDIA_ROOT, SERVER_EMAIL, SITE_NAME

import uuid, requests, tempfile
import datetime, os.path,logging

logger = logging.getLogger(__name__)

def get_location_from_client_ip(request, user):
	try:
		client_ip = get_client_ip(request)
		g = GeoIP()
		client_location = g.city(client_ip)
		if client_location != None:
			user.get_profile().city = client_location['city']
			user.get_profile().country = client_location['country_code']
			if client_location['country_code'] == "US":
				user.get_profile().state = client_location['region']
	except Exception as e:
		logger.exception(e)


class CustomAccountAdapter(DefaultAccountAdapter):

	def render_mail(self, template_prefix, email, context):
		"""
		Renders an e-mail to `email`.  `template_prefix` identifies the
		e-mail that is to be sent, e.g. "account/email/email_confirmation"
		"""
		subject = render_to_string('{0}_subject.txt'.format(template_prefix),
								   context)
		# remove superfluous line breaks
		subject = " ".join(subject.splitlines()).strip()
		subject = self.format_email_subject(subject)

		from_email = SITE_NAME[0].upper() + SITE_NAME[1:].lower() + " <" + SERVER_EMAIL + ">"

		bodies = {}
		for ext in ['html', 'txt']:
			try:
				template_name = '{0}_content.{1}'.format(template_prefix, ext)
				bodies[ext] = render_to_string(template_name,
											   context).strip()
			except TemplateDoesNotExist:
				if ext == 'txt' and not bodies:
					# We need at least one body
					raise
		if 'txt' in bodies:
			msg = EmailMultiAlternatives(subject,
										 bodies['txt'],
										 from_email,
										 [email])
			if 'html' in bodies:
				msg.attach_alternative(bodies['html'], 'text/html')
		else:
			msg = EmailMessage(subject,
							   bodies['html'],
							   from_email,
							   [email])
			msg.content_subtype = 'html'  # Main content is now text/html
		return msg

	def send_mail(self, template_prefix, email, context):
		prefix = "texts/email/apps/account/"
		if "/" in template_prefix:
			template_prefix = prefix + template_prefix[template_prefix.rfind("/")+1:]
		else:
			template_prefix = prefix + template_prefix
		msg = self.render_mail(template_prefix, email, context)
		msg.send()

	def save_user(self, request, user, form):
		data = form.cleaned_data
		email = data['email']
		first_name = data["first_name"]
		last_name = data["last_name"]
		username = generate_unique_username([first_name,last_name,email,'user'])
		gender = data['gender']
		user_email(user, email)
		user_username(user, username)
		user_field(user, 'first_name', first_name or '')
		user_field(user, 'last_name', last_name or '')
		password = data.get("password1")
		if password:
			user.set_password(password)
		else:
			user.set_unusable_password()
		user.save()
		user.get_profile().gender = gender
		avatar = None
		if gender == "m":
			avatar = Photo.objects.create(caption=first_name + " " + last_name + " Avatar", \
							user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_male_icon'],
							unique_id=generate_unique_id("photo"),photo_type='user_profile')
		else:
			avatar = Photo.objects.create(caption=first_name + " " + last_name + " Avatar", \
							user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_female_icon'],
							unique_id=generate_unique_id("photo"),photo_type='user_profile')
		
		cover_picture = Photo.objects.create(caption=first_name + " " + last_name + " Cover Picture", \
							user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_cover_picture'],
							unique_id=generate_unique_id("photo"),photo_type='user_profile')

		get_location_from_client_ip(request,user)
		user.get_profile().avatar = avatar
		user.get_profile().cover_picture = cover_picture
		user.get_profile().save()
		return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

	def populate_user(self,request,sociallogin,data):
		socialaccount = sociallogin.account
		username = data.get('username')
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		name = data.get('name')
		user = sociallogin.account.user
		user_model = get_user_model()

		try:
			query = {"username" + '__iexact': username}
			user_model.objects.get(**query)
			user_username(user,generate_unique_username([first_name,last_name,email,'user']))
		except Exception as e:
			if username == None:
				user_username(user,generate_unique_username([first_name,last_name,email,'user']))
			else:
				user_username(user,username.replace(".",""))

		user_email(user, valid_email_or_none(email) or '')
		name_parts = (name or '').partition(' ')
		user_field(user, 'first_name', first_name or name_parts[0])
		user_field(user, 'last_name', last_name or name_parts[2])
		return user

	def save_user(self, request, sociallogin, form=None):
		socialaccount = sociallogin.account
		user = sociallogin.account.user
		user.set_unusable_password()
		user.save()

		try:            
			birthday = socialaccount.extra_data['birthday']
			month = int(birthday[0:2])
			day = int(birthday[3:5])
			year = int(birthday[6:])
			user.get_profile().birthday = datetime.date(year,month,day)
		except Exception as e:
			logger.exception(e)
			
		gender = socialaccount.extra_data['gender'] 
		user.get_profile().gender = GENDER_MAP_BY_NAME[gender]
		user.get_profile().facebook_id = socialaccount.uid

		# Download Facebook Profile Picture and store it
		try:
			file_name = "facebook_user_" + str(socialaccount.extra_data['id']) + "_avatar.jpg" 
			image_request = requests.get("http://graph.facebook.com/" + socialaccount.uid + "/picture?width=1000&height=1000", stream=True)
			image_file = tempfile.NamedTemporaryFile()
			for block in image_request.iter_content(1024 * 8):
				if not block:
					break
				image_file.write(block)
			image_file.name = file_name
			avatar = Photo.objects.create(caption=str(user.username) + " Avatar",
												  user_post=user,image=files.File(image_file),
												  unique_id=generate_unique_id("photo"),photo_type='user_profile')
			user.get_profile().avatar = avatar
		except Exception as e:
			logger.exception(e)
			avatar = None
			if gender == "m":
				avatar = Photo.objects.create(caption=first_name + " " + last_name + " Avatar", \
								user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_male_icon'],
								unique_id=generate_unique_id("photo"),photo_type='user_profile')
			else:
				avatar = Photo.objects.create(caption=first_name + " " + last_name + " Avatar", \
								user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_female_icon'],
								unique_id=generate_unique_id("photo"),photo_type='user_profile')
			user.get_profile().avatar = avatar


		cover_picture = Photo.objects.create(caption=user.get_profile().get_user_fullname() + " Cover Picture", \
							user_post=user,image=DEFAULT_IMAGE_PATH_MAPPING['default_cover_picture'],
							unique_id=generate_unique_id("photo"),photo_type='user_profile')

		user.get_profile().cover_picture = cover_picture
		get_location_from_client_ip(request,user)
		user.get_profile().save()
		if form:
			email = form.cleaned_data['email']
			user.email = email
			user.save()
		else:
			get_account_adapter().populate_username(request, user)
		sociallogin.save(request)

		SocialFriendList.objects.get_or_create_with_social_auth(socialaccount)

		return user
