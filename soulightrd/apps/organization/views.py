from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, ListView
from django import db

from soulightrd.apps.app_helper import generate_unique_id, get_template_path, get_user_login_object
from soulightrd.apps import AppBaseView

from soulightrd.apps.main.models import Organization, Project, OrganizationBoardMember
from soulightrd.apps.main.constants import ORGANIZATION_FOUNDER
from soulightrd.apps.organization.forms import OrganizationSignUpForm, OrganizationUpdateForm
from soulightrd.apps.alarm import Alarm

from cities_light.models import City

import json, logging, datetime

logger = logging.getLogger(__name__)

alarm = Alarm(logger)

APP_NAME = "organization"

class DetailOrganizationView(DetailView, AppBaseView):
	app_name = APP_NAME
	template_name = "detail"

	def get_object(self, queryset=None):
		''' Return Verified Organization '''
		organization = get_object_or_404(Organization
			, unique_id=self.kwargs.get("organization_unique_id"))
		'''if organization.is_verified == False:
			raise Http404()
		else:'''
		return organization

	def get_context_data(self, **kwargs):
		ctx = super(DetailOrganizationView, self).get_context_data(**kwargs)
		ctx['projects'] = get_list_or_404(Project, organization=ctx['object'])
		ctx['users'] = OrganizationBoardMember.objects.filter(
			organization=ctx['object'])
		return ctx

organization_detail = DetailOrganizationView.as_view()

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
			send_mail("Register new organization", "I would like to apply a new organization"
				, user_login.email, ["soulightrd@gmail.com"])
			return super(CreateOrganizationView, self).form_valid(form)
		except Exception as e:
			alarm.run("Fail to create organization",self.request,e)
			self.handle_fail_request()

create_organization = CreateOrganizationView.as_view()

class ListOrganizationView(ListView, AppBaseView):
	app_name = APP_NAME
	template_name = "list_organization"
	model = Organization
	paginate_by = 10

list_organization = ListOrganizationView.as_view()

class UpdateOrganizationView(UpdateView, AppBaseView):
	app_name = APP_NAME
	template = "create"
	form_class = OrganizationUpdateForm

	def get_initial(self):
		initial = super(UpdateOrganizationView, self).get_initial()
		initial = initial.copy()
		initial['user'] = get_user_login_object(self.request)
		initial['organization'] = Organization.objects.get(
			unique_id=self.kwargs['organization_unique_id'])
		initial['obms'] = OrganizationBoardMember.objects.filter(
			organization=initial['organization'])
		return initial

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		initial_objects = self.get_initial()
		for obm in initial_objects['obms']:
			if obm.user.username == initial_objects['user']:
				return super(UpdateOrganizationView, self).dispatch(*args, **kwargs)
			else:
				return Http404()

	def form_valid(self, form):
		try:
			update_organization_form = form.cleaned_data
			self.organization.name = update_organization_form['name']
			self.organization.description = update_organization_form['description']
			self.organization.website = update_organization_form['website']
			self.organization.email = update_organization_form['email']
			self.organization.phone = update_organization_form['phone']
			self.organization.address = update_organization_form['address']
			self.organization.city = update_organization_form['city']
			self.organization.save()
			return super(UpdateOrganizationView, self).form_valid(form)
		except Exception as e:
			alarm.run("Fail to update organization", self.request, e)
			self.handle_fail_request()

edit_organization = UpdateOrganizationView.as_view()

@login_required
def delete_organization(request):
	return HttpResponse("Delete organization Page")