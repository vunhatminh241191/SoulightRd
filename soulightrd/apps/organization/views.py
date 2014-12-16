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
from django.core.urlresolvers import reverse

from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, ListView, DeleteView, TemplateView
from django.views.generic import View
from django import db
from django.core.urlresolvers import reverse_lazy


from soulightrd.apps.app_helper import generate_unique_id, get_template_path, get_user_login_object
from soulightrd.apps import AppBaseView
from soulightrd.apps.main.models import Organization, Project, OrganizationBoardMember
from soulightrd.apps.main.models import Donation, Rating, Volunteer
from soulightrd.apps.main.constants import ORGANIZATION_FOUNDER
from soulightrd.apps.organization.forms import OrganizationSignUpForm, OrganizationUpdateForm
from soulightrd.apps.alarm import Alarm

from cities_light.models import City
from moneyed import Money

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
		ctx['board_members'] = self.get_organization_board_member_user(ctx['object'])
		ctx['normal_members'] = ctx['object'].normal_member.all()
		ctx['donation'] = self.get_donation(ctx['projects'])
		ctx['volunteer_members'] = self.get_volunteer(ctx['projects'])
		ctx['rating'] = self.get_rating(ctx['object'])
		return ctx

	def get_organization_board_member_user(self, organization):
		board_users = []
		board_members = get_list_or_404(OrganizationBoardMember, organization=organization)
		for board_member in board_members:
			board_users.append(board_member.user)
		return board_users

	def get_donation(self, projects):
		total = Money(0, 'USD')
		for project in projects:
			list_donation = get_list_or_404(Donation, project=project)
			for donation in list_donation:
				total += donation.amount
		return total

	def get_volunteer(self, projects):
		volunteer_users = []
		for project in projects:
			volunteers = get_list_or_404(Volunteer, project=project)
			for volunteer in volunteers:
				volunteer_users.append(volunteer.user)
		return volunteer_users

	def get_rating(self, organization):
		cur_rating = 0
		list_rating = []
		ratings = get_list_or_404(Rating, object_id=organization.unique_id)
		list_rating.append(len(ratings))
		for rating in ratings:
			cur_rating += rating.rating
		list_rating.append(cur_rating/len(ratings))
		return list_rating

organization_detail = DetailOrganizationView.as_view()

class CreateOrganizationView(AppBaseView,FormView):
	app_name = APP_NAME
	template_name = "create"
	form_class = OrganizationSignUpForm
	success_url = reverse_lazy("/?action=create_organization&result=wait_for_verify")

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(CreateOrganizationView, self).dispatch(*args, **kwargs)

	def get_initial(self):
		initial = {}
		try:
			initial["country"] = Country.objects.get(code2=RequestContext(self.request)['current_country_code'])
		except Exception as e:
			alarm.run("Cannot get user country",self.request,e)
		return initial

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
				#city = City.objects.get(id=create_organization_form['city_pk_value']),
				#city = City.objects.get(display_name=create_organization_form['city'])
				city = City.objects.order_by('?')[0],		# temporary until plug autocomplete
			)
			organization_founder = OrganizationBoardMember.objects.create(
				user=user_login,
				organization=organization,
				role=ORGANIZATION_FOUNDER
			)
			#send_mail("Register new organization", "I would like to apply a new organization", user_login.email, ["soulightrd@gmail.com"])
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

	def get_context_data(self, **kwargs):
		ctx = super(ListOrganizationView, self).get_context_data(**kwargs)
		ctx['list'] = serializers.serialize("json", ctx['object_list'])
		ctx['list_image'] = self.get_image_path(ctx['object_list'])
		return ctx

	def get_image_path(self, list_organization):
		array = []
		for organization in list_organization:
			images = []
			dictionary = {}
			for image in organization.images.all():
				images.append(image.image.url)
			dictionary.update({organization.id:images})
			array.append(dictionary)
		return array

list_organization = ListOrganizationView.as_view()


class UpdateOrganizationView(AppBaseView,FormView):
	app_name = APP_NAME
	template_name = "update"
	form_class = OrganizationUpdateForm
	item = None

	def get_initial(self):
		initial = {}
		try:
			initial["organization_unique_id"]= self.item.unique_id
			initial["name"] = self.item.name
			initial["description"] = self.item.description
			initial["website"] = self.item.website
			initial["email"] = self.item.email
			initial["phone"] = self.item.phone
			initial["address"] = self.item.address
		except Exception as e:
			alarm.run("Fail to initialize data",self.request,e)
		return initial

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		self.item = get_object_or_404(Organization,unique_id=self.kwargs['organization_unique_id'])
		board_members = OrganizationBoardMember.objects.filter(organization=self.item)
		for board_member in board_members:
			if board_member.user == get_user_login_object(self.request):
				return super(UpdateOrganizationView, self).dispatch(*args, **kwargs)
		raise Http404()

	def form_valid(self, form):
		organization = self.item
		try:
			update_organization_form = form.cleaned_data
			organization.name = update_organization_form['name']
			organization.description = update_organization_form['description'][3:-4]
			organization.website = update_organization_form['website']
			organization.email = update_organization_form['email']
			organization.phone = update_organization_form['phone']
			organization.address = update_organization_form['address']
			organization.save()
			db.close_connection()
			return super(UpdateOrganizationView, self).form_valid(form)
		except Exception as e:
			alarm.run("Fail to update organization", self.request, e)
			self.handle_fail_request()

	def get_success_url(self):
		return reverse_lazy('organization_detail'
			,kwargs={'organization_unique_id': self.item.unique_id})

edit_organization = UpdateOrganizationView.as_view()

class DeleteOrganizationView(DeleteView, AppBaseView):
	app_name = APP_NAME
	template_name = "delete"
	item = None

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		self.item = get_object_or_404(Organization
			, unique_id=self.kwargs['organization_unique_id'])
		board_members = OrganizationBoardMember.objects.filter(
			organization=self.item)
		for board_member in board_members:
			if board_member.user == get_user_login_object(self.request):
				return super(DeleteOrganizationView, self).dispatch(
					*args, **kwargs)
		return Http404()

	def get_object(self, queryset=None):
		return self.item

	def post(self, request, *args, **kwargs):
		projects = Project.objects.filter(organization=self.item)
		for project in projects:
			project.delete()
		return super(DeleteOrganizationView, self).delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('list_organization')

delete_organization = DeleteOrganizationView.as_view()

class InvitingMember(TemplateView, AppBaseView):
	app_name = APP_NAME
	template_name = "inviting"
	item = None

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		self.item = get_object_or_404(Organization
			, unique_id=self.kwargs['organization_unique_id'])
		board_members = OrganizationBoardMember.objects.filter(
			organization=self.item)
		for board_member in board_members:
			if board_member.user == get_user_login_object(self.request):
				return super(InvitingMember, self).dispatch(
					*args, **kwargs)
		return Http404()

	def get_context_data(self, **kwargs):
		ctx = super(InvitingMember, self).get_context_data(**kwargs)
		ctx['users'] = User.objects.all()
		return ctx

organization_inviting_member = InvitingMember.as_view()

class RequestJoiningOrganization(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(RequestJoiningOrganization, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		print args
		print kwargs

organization_accepting_member = RequestJoiningOrganization.as_view()