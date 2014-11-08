import logging, os

from django import template
from django.middleware.csrf import get_token
from django.conf import settings
from django.core.files.storage import get_storage_class

from soulightrd.settings import ROOT_PATH, STATIC_URL
from soulightrd.apps.app_helper import read_catalogue

logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag(takes_context=True)
def load_plugin_css(context):
	stage = context['stage']
	if stage == "dev":
		css_plugins = ROOT_PATH + "/assets/static/css/plugins/global/stylesheets/"
		list_file = []
		read_catalogue(list_file,css_plugins)
		result = ""
		for filename in list_file:
			result = result + '<link rel="stylesheet" href="' + STATIC_URL + 'css/plugins/global/stylesheets/' + filename +'" type="text/css" />\n'
		return result

@register.simple_tag(takes_context=True)
def load_global_css(context):
	stage = context['stage']
	if stage == "dev":
		responsive_type = "non_responsive" if context['flavour'] == 'full' else "responsive" 
		css_global = ROOT_PATH + "/assets/static/css/global/" + responsive_type
		result = '<link rel="stylesheet" href="' + STATIC_URL + 'css/global/common.css" type="text/css" />\n'
		for filename in os.listdir(css_global):
			result = result + '<link rel="stylesheet" href="' + STATIC_URL + 'css/global/' + responsive_type + "/" + filename +'" type="text/css" />\n'
		return result

@register.simple_tag(takes_context=True)
def load_plugin_js(context):
	stage = context['stage']
	if stage == "dev":
		js_global = ROOT_PATH + "/assets/static/js/plugins/"
		list_file = []
		read_catalogue(list_file,js_global)
		result = ""
		for filename in list_file:
			result = result + '<script type="text/javascript" src="' + STATIC_URL + 'js/plugins/' + filename +'"></script>\n'
		return result

@register.simple_tag(takes_context=True)
def load_global_js(context):
	stage = context['stage']
	if stage == "dev":
		responsive_type = "non_responsive" if context['flavour'] == 'full' else "responsive" 
		js_global = ROOT_PATH + "/assets/static/js/global/" + responsive_type
		list_file = []
		read_catalogue(list_file,js_global)
		result = ""
		for filename in list_file:
			result = result + '<script type="text/javascript" src="' + STATIC_URL + 'js/global/' + responsive_type + "/" + filename +'"></script>\n'
		return result


@register.simple_tag(takes_context=True)
def load_final_level_js(context):
	stage = context['stage']
	app_name = context['app_name']
	responsive_type = "non_responsive" if context['flavour'] == 'full' else "responsive"
	result = ""
	if stage == "dev":
		result = '<script type="text/javascript" src="' + STATIC_URL + 'js/apps/' + responsive_type + "/" + app_name + '/ajax.js"></script>\n' + \
				 '<script type="text/javascript" src="' + STATIC_URL + 'js/apps/' + responsive_type + "/" + app_name + '/function.js"></script>\n' + \
				 '<script type="text/javascript" src="' + STATIC_URL + 'js/apps/' + responsive_type + "/" + app_name + '/main.js"></script>\n'
	else:
		result = '<script type="text/javascript" src="' + STATIC_URL + 'js/apps/' + app_name + '/prod/frittie.script.' + responsive_type + '.min.js"></script>' 
	return result


@register.simple_tag(takes_context=True)
def load_final_level_css(context):
	stage = context['stage']
	app_name = context['app_name']
	responsive_type = "non_responsive" if context['flavour'] == 'full' else "responsive"
	result = ""
	if stage == "dev":
		result = '<link rel="stylesheet" href="' + STATIC_URL + 'css/apps/' + responsive_type + "/" + app_name + '.css" type="text/css" />'
	else:
		result = '<link rel="stylesheet" href="' + STATIC_URL + 'css/prod/stylesheets/' + app_name + '.' + responsive_type + '.min.css" type="text/css" />' 
	return result




	