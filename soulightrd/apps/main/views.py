from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson, timezone
from django.core import serializers

from soulightrd.apps.app_helper import get_template_path

import logging

logger = logging.getLogger(__name__)

APP_NAME = "main"

class MainBaseView(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(MainBaseView, self).get_context_data(**kwargs)
		context['app_name'] = APP_NAME
		return context


class MainView(MainBaseView,TemplateView):
	def get_template_names(self):
		return [get_template_path(APP_NAME,"index",RequestContext(self.request)['flavour'])]
	

class Error404View(MainBaseView,TemplateView):
	def get_template_names(self):
		return [get_template_path(APP_NAME,"404",RequestContext(self.request)['flavour'])]


class Error500View(MainBaseView,TemplateView):
	def get_template_names(self):
		return [get_template_path(APP_NAME,"500",RequestContext(self.request)['flavour'])]







