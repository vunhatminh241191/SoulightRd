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
from django.views.generic.detail import DetailView

from soulightrd.apps.app_helper import generate_unique_id, get_template_path
from soulightrd.apps import AppBaseView

from soulightrd.apps.main.models import Organization, OrganizationBoardMember
from soulightrd.apps.main.constants import ORGANIZATION_FOUNDER
from soulightrd.apps.organization.forms import OrganizationSignUpForm
from soulightrd.apps.alarm import Alarm

import json, logging, datetime

logger = logging.getLogger(__name__)

alarm = Alarm(logger)

APP_NAME = "organization"

class MainOrganizationView(AppBaseView, DetailView):
	app = APP_NAME
	template_name = "detail"
	success_url = "/?action=detail_organization&result=organization_name"
	model = Organization

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MainOrganizationView, self).dispatch(*args, **kwargs)



class CreateOrganizationView(AppBaseView,FormView):
	app_name = APP_NAME
	template_name = "create"
	form = OrganizationSignUpForm
	success_url = "/?action=create_organization&result=wait_for_verify"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(CreateOrganizationView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		user_login = get_user_login_object(self.request)
		try:
			signup_form = form.cleaned_data
			organization = Organization.objects.create(
				unique_id=generate_unique_id('organization'),
				created_by=user_login,
				name=signup_form['name'],
				description=signup_form['description'],
				website=signup_form['website'],
				phone=signup_form['phone'],
				email=signup_form['email'],
				address=signup_form['address'],
				city = City.objects.get(id=signup_form['city']),
				country = signup_form['country']
			)
			organization_founder = OrganizationBoardMember.objects.create(
				user=user_login,
				organization=organization,
				role=ORGANIZATION_FOUNDER
			)
			return super(CreateOrganizationView, self).form_valid(form)
		except Exception as e:
			alarm.run("Fail to create organization",self.request,e)
			self.handle_fail_request()

create_organization = CreateOrganizationView.as_view()


@login_required
def edit_organization(request):
	return HttpResponse("Edit organization Page")



@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")






