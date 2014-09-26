from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.utils import simplejson
from django.core import serializers
from django.contrib.auth.decorators import login_required

import logging, json, datetime

logger = logging.getLogger(__name__)

APP_NAME = "member"

@login_required
def main_page(request, username):
	return HttpResponse("member main page")

@login_required
def settings_page(request):
	return HttpResponse("member setting page")



