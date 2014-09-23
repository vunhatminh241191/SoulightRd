from django import forms
from django.utils.translation import pgettext, ugettext_lazy as _, ugettext
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from django.utils.importlib import import_module

from allauth.account.forms import SignupForm as AccountSignupForm
from allauth.account.forms import SetPasswordField, PasswordField
from allauth.account.forms import ResetPasswordForm

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account import app_settings

from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from allauth.utils import email_address_exists

from soulightrd.apps.main.constants import GENDER
from soulightrd.settings import WEBSITE_HOMEPAGE

class CustomSignupForm(AccountSignupForm):
    first_name = forms.CharField(
        label = _("Firstname"),
        max_length = 40,
        widget = forms.TextInput()
    )
    last_name = forms.CharField(
        label = _("Lastname"),
        max_length = 40,
        widget = forms.TextInput()
    )
    email = forms.EmailField(max_length=60,widget=forms.TextInput())
    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Confirm Password"))
    gender = forms.CharField(label='Gender',required=False,max_length=10,widget=forms.Select(choices=GENDER))

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


