from django.views.generic import ListView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson, timezone
from django.core import serializers

from soulightrd.apps.app_helper import get_template_path
from soulightrd.apps import AppBaseView

import logging

logger = logging.getLogger(__name__)

APP_NAME = "main"


class MainView(AppBaseView,TemplateView):
	app_name = APP_NAME
	template_name = "index"
	

class Error404View(AppBaseView,TemplateView):
	app_name = APP_NAME
	template_name = "404"


class Error500View(AppBaseView,TemplateView):
	app_name = APP_NAME
	template_name = "500"







