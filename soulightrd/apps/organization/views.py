from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import DetailView, ListView
from django import db

from soulightrd.apps.app_helper import generate_unique_id, get_template_path, get_user_login_object
from soulightrd.apps import AppBaseView

from soulightrd.apps.main.models import Organization, OrganizationBoardMember
from soulightrd.apps.main.constants import ORGANIZATION_FOUNDER
from soulightrd.apps.organization.forms import OrganizationSignUpForm
from soulightrd.apps.alarm import Alarm

from cities_light.models import City

import json, logging, datetime

logger = logging.getLogger(__name__)

alarm = Alarm(logger)

APP_NAME = "organization"

class MainOrganizationView(DetailView, AppBaseView):
	app_name = APP_NAME
	template_name = "detail"

	def get_object(self, queryset=None):
		''' Return Verified Organization '''
		organization = get_object_or_404(Organization
			, unique_id=self.kwargs.get("organization_unique_id"))
		if organization.is_verified == False:
			raise Http404()
		else:
			return organization

organization_main = MainOrganizationView.as_view()

class ListOrganizationView(ListView,AppBaseView):
	app_name = APP_NAME
	template_name = "list"


class CreateOrganizationView(AppBaseView,FormView):
	app_name = APP_NAME
	template_name = "create"
	form_class = OrganizationSignUpForm
	success_url = "/?action=create_organization&result=wait_for_verify"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(CreateOrganizationView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		user_login = get_user_login_object(self.request)
		try:
			create_organization_form = form.cleaned_data
			organization = Organization.objects.create(
				unique_id=generate_unique_id('organization'),
				created_by=user_login,
				name=create_organization_form['name'],
				description=create_organization_form['description'],
				website=create_organization_form['website'],
				phone=create_organization_form['phone'],
				email=create_organization_form['email'],
				address=create_organization_form['address'],
				city = City.objects.get(display_name=create_organization_form['city'])
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

class ListProjectView(ListView, AppBaseView):
	app_name = APP_NAME
	template_name = "list_project"
	model = OrganizationBoardMember
	paginate_by = 20

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ListProjectView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		self.tc = get_object_or_404(Organization, unique_id=self.kwargs['organization_unique_id'])
		return OrganizationBoardMember(organization=self.tc)

	def get_context_data(self, **kwargs):
		ctx = super(ListProjectView, self).get_context_data(**kwargs)
		ctx['tc'] = self.tc
		return ctx

list_projects = ListProjectView.as_view()


@login_required
def edit_organization(request):
	return HttpResponse("Edit organization Page")



@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")