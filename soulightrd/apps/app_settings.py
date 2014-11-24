from soulightrd.settings import SITE_NAME, FACEBOOK_APP_ID

import datetime

LOGO_ICON_URL = "https://soulightrd.s3.amazonaws.com/img/ico/favicon.ico"

SITE_NAME_INITIAL_CAPITAL = SITE_NAME[0].upper() + SITE_NAME[1:]

DEFAULT_LATITUDE = 47.616000
DEFAULT_LONGITUDE = -122.322464
DEFAULT_CITY = "Seattle"
DEFAULT_COUNTRY = "United States"
DEFAULT_COUNTRY_CODE = "US"
DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_SERVER_EMAIL = "soulightrd@gmail.com"
DEFAULT_SITE_NAME = 'soulightrd'

SITE_DATA = {
  "SITE_NAME" : SITE_NAME,
  "SITE_NAME_INITIAL_CAPITAL": SITE_NAME_INITIAL_CAPITAL, 
  "SITE_DESCRIPTION": SITE_NAME_INITIAL_CAPITAL + " is a web application provide users opportunity to connect with other people by joining in activity in their favourite location",
  "FACEBOOK_APP_ID": FACEBOOK_APP_ID,
  "DEFAULT_TIMEZONE": DEFAULT_TIMEZONE
}

KEYWORDS_URL = [
	'admin','signup','login','password',"accounts"
	'logout','confirm_email','search','settings',
	'buzz','messages',"about",'api','asset','photo',
	'feeds','friends'
]

MODEL_KEY_LIST = [
  "OR", "PJ", "PA", "IV", "PT", "CM", "CN", "RP", "NF", "MG", "FD", "DI", "UN"
]

MODEL_KEY_MAP = {
  "organization": "OR",
  "project": "PJ",
  "project_activity": "PA",
  "invitation": "IV",
  "photo": "PT",
  "comment": "CM",
  "conversation": "CN",
  "report": "RP",
  "notification": "NF",
  "message": "MG",
  "feed": "FD",
  "default_image": "DI",
}

UNSPECIFIED_MODEL_KEY = "UN"


DEFAULT_IMAGE_PATH_MAPPING = {

  # User Image
  "default_male_icon": "default/img/user/male_icon.png",
  "default_female_icon": "default/img/user/female_icon.png",
  "default_cover_picture": 'default/img/user/cover_picture.png',
  "default_project_picture": 'default/img/user/project_picture.png',
  "default_project_activity_picture": 'default/img/user/project_activity_picture.png',
}


DEFAULT_IMAGE_UNIQUE_ID = {

  "default_male_icon": "DIBHgn2pXkaWLAYgpRsQGTo3088",
  "default_female_icon": "DIJE4S63KnuKozEq4BsC2PH4019",
  "default_cover_picture": 'DInXsK7dXR9BGXpmKR9Mhd6D124',
  "default_project_picture": 'DInXsK7dXR9BGXpmKR9Mhd7B89',
  "default_project_activity_picture": 'DInXsK7dXR9BGXpmKR9Mhd2M33',
}

MESSAGE_SNIPPET_TEMPLATE =  { 
  # Auth app
  "signup_success": "messages/apps/auth/signup_success.html",
  "confirm_email_success": "messages/apps/auth/confirm_email_success.html",
  "confirm_email_asking": "messages/apps/auth/confirm_email_asking.html",
  "resend_confirm_email_success": "messages/apps/auth/resend_confirm_email_success.html",
  "resend_confirm_email_error": "messages/apps/auth/resend_confirm_email_error.html",
  "change_password_success": "messages/apps/auth/change_password_success.html",
  "social_login_error": "messages/apps/auth/social_login_error.html",
  "reset_password_success": "messages/apps/auth/reset_password_success.html",
}

HTML_SNIPPET_TEMPLATE = {
  

}

EMAIL_SUBJECT_SNIPPET_TEMPLATE = {


}

EMAIL_CONTENT_HTML_SNIPPET_TEMPLATE = {
 "organization_register": "organization-register"
  
}

EMAIL_CONTENT_TEXT_SNIPPET_TEMPLATE = {
 
}


