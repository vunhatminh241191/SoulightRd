from django import forms
from django.utils.translation import pgettext, ugettext_lazy as _, ugettext
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from django.utils.importlib import import_module

from allauth.account.forms import SignupForm as AccountSignupForm
from allauth.account.forms import LoginForm as AccountLoginForm
from allauth.account.forms import ResetPasswordForm

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod

from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from allauth.utils import email_address_exists, get_user_model, set_form_field_order

from soulightrd.apps.main.constants import GENDER
from soulightrd.settings import WEBSITE_HOMEPAGE

class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value',
                                  app_settings.PASSWORD_INPUT_RENDER_VALUE)
        kwargs['widget'] = forms.PasswordInput(render_value=render_value,
                                               attrs={'placeholder':
                                                      _('Password'), "class": "form-control"})
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):

    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if len(value) < min_length:
            raise forms.ValidationError(_("Password must be a minimum of {0} "
                                          "characters.").format(min_length))
        return value


class CustomLoginForm(AccountLoginForm):

    password = PasswordField(label=_("Password"))
    remember = forms.BooleanField(label=_("Remember Me"),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('E-mail address'), 'autofocus': 'autofocus','class':'form-control'})
            login_field = forms.EmailField(label=_("E-mail"),
                                           widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username'), 'autofocus': 'autofocus','class':'form-control'})
            login_field = forms.CharField(label=_("Username"),
                                          widget=login_widget,
                                          max_length=30)
        else:
            assert app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME_EMAIL
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username or e-mail'), 'autofocus': 'autofocus','class':'form-control'})
            login_field = forms.CharField(label=pgettext("field label",
                                                         "Login"),
                                          widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self,  ["login", "password", "remember"])

class CustomSignupForm(AccountSignupForm):
    first_name = forms.CharField(
        label = _("Firstname"),
        max_length = 40,
        widget = forms.TextInput(attrs={'placeholder': 'First Name', 'class': "form-control"})
    )
    last_name = forms.CharField(
        label = _("Lastname"),
        max_length = 40,
        widget = forms.TextInput(attrs={'placeholder': 'Last Name','class': "form-control"})
    )
    email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder': 'Email','class': "form-control"}))
    password1 = SetPasswordField(label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': "form-control"}))
    #gender = forms.CharField(label='Gender',required=False,max_length=10,widget=forms.Select(choices=GENDER))

    def clean_email(self):
        value = self.cleaned_data["email"]
        if app_settings.UNIQUE_EMAIL:
            if value and email_address_exists(value):
                raise forms.ValidationError \
                    (_("Unavailable Email Address"))
        return value


class CustomResetPasswordForm(ResetPasswordForm):

    def save(self, **kwargs):

        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            current_site = Site.objects.get_current()

            # send the password reset email
            path = reverse("account_reset_password_from_key",
                           kwargs=dict(uidb36=int_to_base36(user.id),
                                       key=temp_key))
            url = '%s%s' % (WEBSITE_HOMEPAGE, path[1:])
            context = {"site": current_site,
                       "user": user,
                       "password_reset_url": url}
            get_adapter().send_mail('account/email/password_reset_key',
                                    email,
                                    context)
        return self.cleaned_data["email"]


class CustomSocialSignupForm(SocialSignupForm):

    def raise_duplicate_email_error(self):
        raise forms.ValidationError("This email address is not available.")


