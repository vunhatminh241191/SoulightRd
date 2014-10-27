from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from soulightrd.apps.app_helper import generate_unique_id, get_template_path

from soulightrd.apps.main.models import Organization
from . import forms

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "organization"

def main_page(request):
	return HttpResponse("Projet Main Page")


class CreateOrganizationView(FormView):
	form_class = forms.OrganizationSignUpForm

	def form_valid(self, form):
		beta_form = form.cleaned_data
		organization = Organization.objects.create(
			unique_id=generate_unique_id("organization"),
			created_by=self.request.user,
			name=beta_form["name"],
			description=beta_form["description"],
			phone=beta_form["phone"],
			email=beta_form["email"],
			address=beta_form["address"],
			organization_date=datetime.datetime.now())
		return super(CreateOrganizationView, self).form_valid(form)

	def form_invalid(self, form):
		print "hehehehe"
		return super(CreateOrganizationView, self).form_invalid(form)

	def get_success_url(self):
		return HttpResponse("home")

	def get_context_data(self, **kwargs):
		print kwargs["form"]
		ret = super(CreateOrganizationView, self).get_context_data(**kwargs)
		ret["app_name"] = APP_NAME
		return ret

	def get_template_names(self):		
		template_path = get_template_path(APP_NAME,"signup",RequestContext(self.request)['flavour'],'/page/')
		return [template_path]

create_organization = CreateOrganizationView.as_view()

@login_required
def edit_organization(request):
	return HttpResponse("Edit organization Page")


@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")






