from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from soulightrd.apps.main.models import Organization
from cities_light.models import City
from django.contrib.auth.models import User

class OrganizationSignUpForm(forms.Form):
	name = forms.CharField(
			label = _("Organization Name"), max_length = 50,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'
				, 'class': "form-control"})
		)
	description = forms.CharField(
			label = _("Description Organization"), max_length= 500,
			widget = forms.TextInput(attrs={'placeholder': 'Tell us more about your organization'
				, 'class': "form-control"})
		)
	website = forms.URLField(
			label = _("Organization Website"), max_length= 30, required=False,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization website'
				, 'class': "form-control"})
		)
	email = forms.EmailField(
			label = _("Organization Email"), max_length= 100,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'
				, 'class': "form-control"})
		)
	phone = forms.CharField(label = _("Organization Phone"),
			widget = forms.TextInput(attrs={'placeholder': 'Your organization phone number'
				, 'class': "form-control"})
		)
	address = forms.ModelChoiceField(queryset=City.objects.all(),
			label = _("Organization Address")
		)
	normal_member = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
			label = _("Invite Member")
		)

	def __init__(self, *args, **kwargs):
		super(OrganizationSignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'signup_form'
		self.helper.form_class = 'signup'
		self.helper.form_method = 'post'
		self.helper.form_action = 'create_organization'
		self.helper.add_input(Submit('submit', 'Submit'))
