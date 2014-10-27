from django import forms
from django.utils.translation import ugettext_lazy as _
from localflavor.us.forms import USPhoneNumberField

from soulightrd.apps.main.models import Organization
from cities_light.models import City
from django.contrib.auth.models import User

class USPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits US Phone number input into three <input type='text'> boxes.
    """
    def __init__(self,attrs=None):
        widgets = (
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone'}),
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone'}),
            forms.TextInput(attrs={'size':'4','maxlength':'4', 'class':'phone'}),
        )
        super(USPhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split('-')
        return (None,None,None)

    def value_from_datadict(self, data, files, name):
        value = [u'',u'',u'']
        # look for keys like name_1, get the index from the end
        # and make a new list for the string replacement values
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name)+1:]) 
            value[index] = data[d]
        if value[0] == value[1] == value[2] == u'':
            return None
        return u'%s-%s-%s' % tuple(value)

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
			label = _("Organization Website"), max_length= 100,
			widget = forms.TextInput(attrs={'placeholder': 'Your organization email'
				, 'class': "form-control"})
		)
	phone = USPhoneNumberField(label = _("Organization Phone"),
			widget=USPhoneNumberMultiWidget()
		)
	address = forms.ModelChoiceField(queryset=City.objects.all(),
			label = _("Organization Address")
		)
	normal_member = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
			label = _("Invite Member")
		)