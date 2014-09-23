from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "main"

def main_page(request):
	return HttpResponse("HELLO WORLD")

# This will show a general page for all kind of error
def error_page(request):
	return render_to_response("error.html",{},context_instance=RequestContext(request))




