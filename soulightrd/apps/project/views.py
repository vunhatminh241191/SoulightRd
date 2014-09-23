from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.contrib.auth.decorators import login_required

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "project"

def main_page(request):
	return HttpResponse("Project Main Page")


@login_required
def create_project(request):
	return HttpResponse("Create Project Page")


@login_required
def edit_project(request):
	return HttpResponse("Edit Project Page")


@login_required
def delete_project(request):
	return HttpResponse("Delete Project Page")






