from django.contrib.gis.geoip import GeoIP

from soulightrd.apps.app_settings import SITE_DATA, DEFAULT_LATITUDE
from soulightrd.apps.app_settings import DEFAULT_LONGITUDE, DEFAULT_CITY
from soulightrd.apps.app_settings import DEFAULT_COUNTRY

from soulightrd.settings import SITE_NAME, STAGE

from soulightrd.apps.app_helper import handle_request_get_message, get_user_login_object
from soulightrd.apps.app_helper import capitalize_first_letter, get_client_ip

from soulightrd.apps.auth.helper import activate_email_reminder_message

import datetime

def site_data(request):
	return SITE_DATA 

def global_data(request):
	results = {}
	client_ip = get_client_ip(request)
	results['client_ip'] = client_ip
	g = GeoIP()
	results['current_lat'] = DEFAULT_LATITUDE
	results['current_lng'] = DEFAULT_LONGITUDE
	results['current_city'] = DEFAULT_CITY
	results['current_country'] = DEFAULT_COUNTRY
	results['geo_data'] = None
	if g.city(client_ip) != None:
		geo_data = g.city(client_ip)
		results['current_lat'] = geo_data['latitude']
		results['current_lng'] = geo_data['longitude']
		results['current_city'] = geo_data['city']
		results['current_country'] = geo_data['country_name']
		results['geo_data'] = geo_data
	results['user_login'] = get_user_login_object(request)
	activate_message = activate_email_reminder_message(request,results['user_login']) 
	if activate_message == None:
		data = { 'user_login':results['user_login'], 'site_name': capitalize_first_letter(SITE_NAME) }
		results["request_message"] = handle_request_get_message(request,data)
		results['is_activate_message'] = False
	else:
		results["request_message"] = activate_message
		results['is_activate_message'] = True
	results['stage'] = STAGE
	return results


