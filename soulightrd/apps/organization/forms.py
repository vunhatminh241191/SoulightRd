from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from soulightrd.apps.main.models import Organization

from cities_light.models import City

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.layout import Div, HTML, Button, Hidden, Field

from soulightrd.apps.main.models import Organization

from cities_light.models import City, Country

class OrganizationForm(forms.ModelForm):

	name = forms.CharField(
			label = _("Name"),
			widget = forms.TextInput()
		)
	description = forms.CharField(
			label = _("Description "),
			widget = forms.Textarea(attrs={'placeholder': 'Tell us more about your organization',"class": "mce-editor"})
		)
	website = forms.URLField(
			label = _("Website (optional)"), required=False,
			widget = forms.TextInput()
		)
	email = forms.EmailField(
			label = _("Email"),
			widget = forms.TextInput()
		)
	phone = forms.RegexField(label=_("Phone"),max_length=15,
			regex=r'^\+?1?\d{9,15}$', 
			error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
			widget = forms.TextInput())
	address = forms.CharField(label = _("Address"), max_length = 200,
			widget = forms.TextInput(attrs={'placeholder': 'Street address, district, etc'})
		)
	city = forms.CharField(label = _("City"), max_length = 10,
			widget=forms.TextInput()
		)


class OrganizationSignUpForm(OrganizationForm):
	def __init__(self, *args, **kwargs):
		super(OrganizationSignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'create_organization_form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'create_organization'
		self.helper.layout = Layout(
		    'name',
		    'description',
		    'email',
		    'phone',
		    'address',
		    'city',
		    'country',
		    'website',
		    Div(
		    	Div(css_class='col-lg-2'),
		    	ButtonHolder(
		    		Button('cancel', 'Cancel',css_class='btn btn-default btn-sm pull-right mini-margin-left'),
		    		Submit("submit","Submit",css_class="btn btn-primary btn-sm pull-right"),
		    		css_class = 'col-lg-9'
		    	),
		    	css_class = "form-group"
		    ),
		    Hidden("city_pk_value","",id="city_pk_value")
		)

class OrganizationUpdateForm(OrganizationForm):
	def __init__(self, *args, **kwargs):
		super(OrganizationUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'edit_organization_form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'edit_organization'
		self.helper.layout = Layout(
		    'name',
		    'description',
		    'email',
		    'phone',
		    'address',
		    'city',
		    'country',
		    'website',
		    Div(
		    	Div(css_class='col-lg-2'),
		    	ButtonHolder(
		    		Button('cancel', 'Cancel',css_class='btn btn-default btn-sm pull-right mini-margin-left'),
		    		Submit("submit","Submit",css_class="btn btn-primary btn-sm pull-right"),
		    		css_class = 'col-lg-9'
		    	),
		    	css_class = "form-group"
		    ),
		    Hidden("city_pk_value","",id="city_pk_value")
		)
