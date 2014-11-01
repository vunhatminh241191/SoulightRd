from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from soulightrd.apps.main.models import Organization

from cities_light.models import City

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from soulightrd.apps.main.models import Organization

from cities_light.models import City

from django_countries.widgets import CountrySelectWidget

class OrganizationSignUpForm(forms.Form):
	name = forms.CharField(
			label = _("Name"),
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	description = forms.CharField(
			label = _("Description "),
			widget = forms.TextInput(attrs={'placeholder': 'Tell us more about your organization'})
		)
	website = forms.URLField(
			label = _("Website"), required=False,
			widget = forms.TextInput(attrs={'placeholder': 'Website'})
		)
	email = forms.EmailField(
			label = _("Email"),
			widget = forms.TextInput(attrs={'placeholder': 'Email'})
		)
	phone = forms.RegexField(label=_("Phone"),max_length=15,
			regex=r'^\+?1?\d{9,15}$', 
			error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
			widget = forms.TextInput(attrs={'placeholder': 'Phone Number'}))
	address = forms.CharField(label = _("Address"), max_length = 200,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'})
		)
	city = forms.CharField(label = _("City"), max_length = 10,
			widget=forms.TextInput(attrs={'placeholder': "City"})
		)
	country = forms.CharField(label= _("Country"),
			widget=CountrySelectWidget
		)
	normal_member = forms.ModelMultipleChoiceField(label = _("Invite Member"),
		queryset=User.objects.all())


	def __init__(self, *args, **kwargs):
		super(OrganizationSignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'signup_form'
		self.helper.form_class = 'signup'
		self.helper.form_method = 'post'
		self.helper.form_action = 'create_organization'
		self.helper.add_input(Submit('submit', 'Submit'))
