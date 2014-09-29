from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext

from django.conf import settings as django_settings
from django.utils.html import strip_tags

from soulightrd.apps.app_settings import MODEL_KEY_MAP, UNSPECIFIED_MODEL_KEY, MODEL_KEY_LIST
from soulightrd.apps.app_settings import MESSAGE_SNIPPET_TEMPLATE, HTML_SNIPPET_TEMPLATE
from soulightrd.settings import SITE_NAME, ADMINS_USERNAME, SECRET_KEY, OW_LY_API_KEY

from firebase_token_generator import create_token

import collections, datetime, decimal, json, os, logging
import shortuuid, random, math, pycountry, pytz, requests

logger = logging.getLogger(__name__)

CATALOGUE = "CATALOGUE"
COMMENT_CHARACTER = "<!--"


def read_catalogue(list_file,path):
	catalogue_path = path
	if CATALOGUE not in path:
		catalogue_path = path + CATALOGUE if path[len(path)-1] == "/" else path + "/" + CATALOGUE
	f = open(catalogue_path,"r")
	for filename in f:
		if len(filename.replace("\n","")) != 0 and filename.startswith(COMMENT_CHARACTER) == False:
			list_file.append(filename.replace("\n",""))

def make_two_numbers(original):
	if len(original)==1:
		return "0"+original
	else:
		return original

def capitalize_first_letter(s):
	if s == None: return
	if len(s) == 0: return
	return s[0].upper() + s[1:].lower()


def json_encode_decimal(obj):
	if isinstance(obj, decimal.Decimal):
		return str(obj)
	raise TypeError(repr(obj) + " is not JSON serializable")


def convert_24hr_to_ampm(time):
	hour = time.hour
	minute = time.minute
	if int(hour) >= 12:
		final_hour = int(hour) + 1 - 12
		return str("%02d" % final_hour) + ":" + str("%02d" % minute) + "pm"
	else:
		return str("%02d" % hour) + ":" + str("%02d" % minute) + "am"


def convert_ampm_to_24hr(time,ampm):
	hour = time.hour
	result = ""
	if ampm.lower() == 'am':
		if int(hour) == 12: 
			result = "00:"
		else: 
			result = make_two_numbers(hour) + ":"
	if ampm.lower() == 'pm':
		if int(hour) == 12: 
			result = "12:"
		else: 
			result = str(12 + hour) + ":"
	return result + str(time.minute) + " " + ampm
  

def get_duplicate_object(l):
	l2 = collections.Counter(l)
	return [i for i in l2 if l2[i]>1]


def remove_duplicate_object(l):
	return list(set(l))


def set_fixed_string(s,s_len):
	if s_len >= len(s): 
		return s
	return s[:s_len] + '...'


# Get current login user object
def get_user_login_object(request):
	user_login = request.user
	if user_login.is_anonymous():
		return None
	return user_login


# Get the current ip from client to see their zip code and
# return appropriate location. Currently, this is not work with localhost
def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


# Setup the constant month tuple using for the form
def setup_constant_month():
	month_value = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	l = []
	for i in range(1,13):
		l.append([i,month_value[i-1]])
	return tuple(tuple(x) for x in l)


# Setup the constant day tuple 
def setup_constant_day():
	l = []
	for i in range(1,32):
		l.append([i,i])
	return tuple(tuple(x) for x in l)


# Setup the constant year tuple 
def setup_constant_year():
	l = []
	current_year = datetime.datetime.now().year
	for i in range(1920,int(current_year) - 13):
		l.append([i,i])
	return tuple(tuple(x) for x in l)


# Setup the constant countries in alpha2 code
def setup_constant_countries_alpha2():
	output = []
	for country in list(pycountry.countries):
		data = (str(country.alpha2),country.name.encode("utf-8"))
		output.append(data)
	return tuple(output)	


# Setup the constant countries in alpha3 code
def setup_constant_countries_alpha3():
	output = []
	for country in list(pycountry.countries):
		data = (str(country.alpha3),country.name.encode("utf-8"))
		output.append(data)
	return tuple(output)	


def generate_html_snippet(request,snippet,data):
	return render_to_response(HTML_SNIPPET_TEMPLATE[snippet],data,context_instance=RequestContext(request)).content
	

def generate_message(action,result,data):
	template_name = action + "_" + result
	message = render_to_string(MESSAGE_SNIPPET_TEMPLATE[template_name],data)
	return message


def handle_request_get_message(request,data):
	if request.session.get('is_show_request_message'):
		del request.session['is_show_request_message']
		if "action" in request.GET and "result" in request.GET:	
			return generate_message(request.GET['action'],request.GET['result'],data)
	return None


def generate_unique_id(model_type=None):
	prefix = UNSPECIFIED_MODEL_KEY
	if model_type != None:
		if model_type.lower() in MODEL_KEY_MAP:
			prefix = MODEL_KEY_MAP[model_type.lower()]
	return prefix + shortuuid.uuid()[:11] + shortuuid.uuid()[:11] + str("%03d" % random.randint(1,999))


def get_any_admin_object():
	for username in ADMINS_USERNAME:
		try:
			admin = User.objects.get(username=username)
			return admin
		except User.DoesNotExist:
			pass
	return None


def generate_token(custom_data,options):
	return create_token(SECRET_KEY,custom_data,options)


def get_short_url(request):
	long_url = str(request.build_absolute_uri())
	try:
		r = requests.get("http://ow.ly/api/1.1/url/shorten?apiKey=" + OW_LY_API_KEY + "&longUrl=" + long_url)
		data = r.json()
		return data['results']['shortUrl']
	except:
		pass	
	return long_url
	
def get_different_hours_from_timezones(first,second):
	try:
		if (TIMEZONE_TO_UTC[str(second)] is not None ) and (TIMEZONE_TO_UTC[str(first)] is not None):
			return TIMEZONE_TO_UTC[str(second)]-TIMEZONE_TO_UTC[str(first)]
	except:
		pass
	return 0

def is_str_unique_id(s):
	if len(s) != 27 or s[24:27].isdigit() == False or s[0:2].upper() not in MODEL_KEY_LIST: 
		return False
	return True


def get_template_path(app_name,template_name,flavour,sub_path='/page/'):
	if flavour == None:
		return "sites/non-responsive/apps/" + app_name + sub_path + template_name + ".html"
	else:
		prefix = "non_responsive" if flavour == "full" else "responsive"
		return "sites/" + prefix + "/apps/" + app_name + sub_path + template_name + ".html"



