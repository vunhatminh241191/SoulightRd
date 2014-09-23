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

APP_NAME = "organization"

def main_page(request):
	return HttpResponse("Projet Main Page")


@login_required
def create_organization(request):
	return HttpResponse("Create organization Page")


@login_required
def edit_organization(request):
	return HttpResponse("Edit organization Page")


@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")






