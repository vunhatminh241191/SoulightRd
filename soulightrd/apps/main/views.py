###############################
#  Author: Dang Nguyen,Duc Vu #
#  Date: 5/24/2012            #
#  Last Modified: 10/04/2013  #
###############################

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers

from frittie.apps.app_helper import get_user_login_object, convert_list_to_json, get_template_path
from frittie.apps.activity.helper import get_nearby_activity
from frittie.apps.location.helper import get_nearby_location, get_current_city
from frittie.apps.main.models import Activity, Location, Photo

from frittie.apps.main.constants import PUBLIC, LOCATION_PRIVATE_PLACE
from frittie.apps.app_settings import NUM_ITEM_PER_PAGE

import json, logging, datetime

APP_NAME = "main"

def main_page(request):
	return HttpResponse("HELLO WORLD")

# This will show a general page for all kind of error
def error_page(request):
	return render_to_response("error.html",{},context_instance=RequestContext(request))




