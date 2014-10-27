from django import forms
from django.utils.translation import ugettext_lazy as _

from soulightrd.apps.main.models import Organization

class OrganizationSignUpForm(forms.ModelForm):
	name = forms.CharField(
			label = _("Organizatio Nname"), max_length = 50,
			widget = forms.TextInput(attrs={'placeholder': 'Organization Name'
				, 'class': "form-control"})
		)
	description = forms.CharField(
			label = _("Description Organization"), max_length= 500,
			widget = forms.TextInput(attrs={'placeholder': 'Tell us more about your organization'
				, 'class': "form-control"})
		)
	website = forms.CharField(
			label = _("Organization Website"), max_length= 30, required=False,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization website'
				, 'class': "form-control"})
		)
	email = forms.URLField(
			label = _("Organization Website"), max_length= 100,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'
				, 'class': "form-control"})
		)

	class Meta:
		model = Organization
		fields = ['name', 'description','website', 'email', 'phone', 'address', 'normal_member']