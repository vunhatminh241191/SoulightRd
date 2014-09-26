from soulightrd.settings import SITE_NAME

import datetime

LOGO_ICON_URL = "https://soulightrd.s3.amazonaws.com/img/ico/favicon.ico"

SITE_NAME_INITIAL_CAPITAL = SITE_NAME[0].upper() + SITE_NAME[1:]

DEFAULT_LATITUDE = 47.616000
DEFAULT_LONGITUDE = -122.322464
DEFAULT_CITY = "Seattle"
DEFAULT_COUNTRY = "United States"
DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_SERVER_EMAIL = "team@soulightrd.com"
DEFAULT_SITE_NAME = 'soulightrd'

SITE_DATA = {
  "SITE_NAME" : SITE_NAME,
  "SITE_NAME_INITIAL_CAPITAL": SITE_NAME_INITIAL_CAPITAL, 
  "SITE_DESCRIPTION": SITE_NAME_INITIAL_CAPITAL + " is a web application provide users opportunity to connect with other people by joining in activity in their favourite location",
  #"FACEBOOK_APP_ID": FACEBOOK_APP_ID,
  "DEFAULT_TIMEZONE": DEFAULT_TIMEZONE
}

KEYWORDS_URL = [
	'admin','signup','login','password',"accounts"
	'logout','confirm_email','search','settings',
	'buzz','messages',"about",'api','asset','photo',
	'feeds','friends'
]

MODEL_KEY_LIST = [
  "LO", "AC", "IV", "PT", "VD", "CM", "CN", "RP", "NF", "MG", "FD", "DI", "UN"
]

MODEL_KEY_MAP = {
  "location": "LO",
  "activity": "AC",
  "invitation": "IV",
  "photo": "PT",
  "video": "VD",
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

}


DEFAULT_IMAGE_UNIQUE_ID = {

  "default_male_icon": "DIBHgn2pXkaWLAYgpRsQGTo3088",
  "default_female_icon": "DIJE4S63KnuKozEq4BsC2PH4019",
  "default_cover_picture": 'DInXsK7dXR9BGXpmKR9Mhd6D124',

}

MESSAGE_SNIPPET_TEMPLATE =  { 
 
}

HTML_SNIPPET_TEMPLATE = {
  

}

EMAIL_SUBJECT_SNIPPET_TEMPLATE = {


}

EMAIL_CONTENT_HTML_SNIPPET_TEMPLATE = {

  
}

EMAIL_CONTENT_TEXT_SNIPPET_TEMPLATE = {
 
}


