from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
<<<<<<< HEAD

from soulightrd.apps.main.models import Organization

from cities_light.models import City

from phonenumber_field.modelfields import PhoneNumberField
=======

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from soulightrd.apps.main.models import Organization

from cities_light.models import City
from phonenumber_field.widgets import PhoneNumberPrefixWidget
>>>>>>> remotes/origin/organization_form

from django_countries.widgets import CountrySelectWidget

class OrganizationSignUpForm(forms.Form):
	name = forms.CharField(
<<<<<<< HEAD
			label = _("Name"), max_length = 50,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	description = forms.CharField(
			label = _("Description "), max_length= 1000,
			widget = forms.TextInput(attrs={'placeholder': 'Tell us more about your organization'})
		)
	website = forms.URLField(
			label = _("Website"), max_length= 30, required=False,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization website'})
		)
	email = forms.EmailField(
			label = _("Email"), max_length= 100,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'})
		)
	phone = PhoneNumberField()
	address = forms.CharField(label = _("Address"), max_length = 50,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	city = forms.CharField(label = _("City"), max_length = 300,
			widget=forms.TextInput(attrs={'placeholder': "City"})
		)
	country = forms.CharField(label= _("Country"), max_length = 100,
			widget=CountrySelectWidget
		)

=======
			label = _("Name"),
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	description = forms.CharField(
			label = _("Description "),
			widget = forms.TextInput(attrs={'placeholder': 'Tell us more about your organization'})
		)
	website = forms.URLField(
			label = _("Website"), required=False,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization website'})
		)
	email = forms.EmailField(
			label = _("Email"),
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'})
		)
	phone = forms.CharField(
			label= _("Phone"),
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'})
		)
	address = forms.CharField(label = _("Address"),
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	city = forms.CharField(label = _("City"),
			widget=forms.TextInput(attrs={'placeholder': "City"})
		)
	country = forms.CharField(label= _("Country"),
			widget=CountrySelectWidget
		)


	def __init__(self, *args, **kwargs):
		super(OrganizationSignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'signup_form'
		self.helper.form_class = 'signup'
		self.helper.form_method = 'post'
		self.helper.form_action = 'create_organization'
		self.helper.add_input(Submit('submit', 'Submit'))
>>>>>>> remotes/origin/organization_form
