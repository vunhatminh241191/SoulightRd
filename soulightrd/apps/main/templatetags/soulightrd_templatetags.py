import logging, os

from django import template
from django.middleware.csrf import get_token
from django.conf import settings
from django.core.files.storage import get_storage_class

from soulightrd.settings import ROOT_PATH, STATIC_URL
from soulightrd.apps.app_helper import read_catalogue

logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag
def load_plugin_css():
	css_plugins = ROOT_PATH + "/assets/static/css/plugins/global/stylesheets/"
	list_file = []
	read_catalogue(list_file,css_plugins)
	result = ""
	for filename in list_file:
		result = result + '<link rel="stylesheet" href="' + STATIC_URL + 'css/plugins/global/stylesheets/' + filename +'" type="text/css" />\n'
	return result

@register.simple_tag(takes_context=True)
def load_global_css(context):
	responsive_type = "non_responsive" if context['flavour'] == 'full' else "responsive" 
	css_global = ROOT_PATH + "/assets/static/css/global/" + responsive_type
	result = '<link rel="stylesheet" href="' + STATIC_URL + 'css/global/common.css" type="text/css" />\n'
	for filename in os.listdir(css_global):
		result = result + '<link rel="stylesheet" href="' + STATIC_URL + 'css/global/' + responsive_type + "/" + filename +'" type="text/css" />\n'
	return result

@register.simple_tag
def load_plugin_js():
	js_global = ROOT_PATH + "/assets/static/js/plugins/"
	list_file = []
	read_catalogue(list_file,js_global)
	result = ""
	for filename in list_file:
		result = result + '<script type="text/javascript" src="' + STATIC_URL + 'js/plugins/' + filename +'"></script>\n'
	return result

@register.simple_tag
def load_global_js():
	js_global = ROOT_PATH + "/assets/static/js/global/"
	list_file = []
	read_catalogue(list_file,js_global)
	result = ""
	for filename in list_file:
		result = result + '<script type="text/javascript" src="' + STATIC_URL + 'js/global/' + filename +'"></script>\n'
	return result




	