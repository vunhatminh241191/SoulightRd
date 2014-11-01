from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from soulightrd.apps.main.models import Organization

from cities_light.models import City

from phonenumber_field.modelfields import PhoneNumberField

from django_countries.widgets import CountrySelectWidget

class OrganizationSignUpForm(forms.Form):
	name = forms.CharField(
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
	address = forms.CharField(label = _("Address"), max_length = 200,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	city = forms.CharField(label = _("City"), max_length = 10,
			widget=forms.TextInput(attrs={'placeholder': "City"})
		)
	country = forms.CharField(label= _("Country"), max_length = 100,
			widget=CountrySelectWidget
		)

