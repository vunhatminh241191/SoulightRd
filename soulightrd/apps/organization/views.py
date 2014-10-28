from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from allauth.account.utils import get_next_redirect_url

from soulightrd.apps.app_helper import generate_unique_id, get_template_path

from soulightrd.apps.main.models import Organization
from soulightrd.apps.organization.forms import OrganizationSignUpForm

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "organization"

def main_page(request):
	return HttpResponse("Projet Main Page")


class CreateOrganizationView(FormView):
	form_class = OrganizationSignUpForm
	success_url = "/?action=signup&result=success"
	redirect_field_name = "next"

	def form_valid(self, form):
		beta_form = form.cleaned_data
		organization = Organization.objects.create(
			unique_id=generate_unique_id('organization'),
			created_by=self.request.user,
			name=beta_form['name'],
			description=beta_form['description'],
			website=beta_form['website'],
			phone=beta_form['phone'],
			email=beta_form['email'],
			address=beta_form['address'],
			organization_date=datetime.datetime.now())

		for user in beta_form['normal_member']:
			organization.normal_member.add(user)
		organization.save()
		return super(CreateOrganizationView, self).form_valid(form)

	def get_success_url(self):
		ret = (get_next_redirect_url(self.request,
									 self.redirect_field_name)
			   or self.success_url)
		return ret


	def get_context_data(self, **kwargs):
		ret = super(CreateOrganizationView, self).get_context_data(**kwargs)
		ret["app_name"] = APP_NAME
		return ret

	def get_template_names(self):		
		template_path = get_template_path(APP_NAME,"signup",RequestContext(self.request)['flavour'],'/page/')
		return [template_path]

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(CreateOrganizationView, self).dispatch(*args, **kwargs)

create_organization = CreateOrganizationView.as_view()

@login_required
def edit_organization(request):
	return HttpResponse("Edit organization Page")


@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")






