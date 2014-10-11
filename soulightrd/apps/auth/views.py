from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.sites.models import Site
from django.utils.http import base36_to_int
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.cache import patch_response_headers


from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_user_model

from allauth.account.utils import (get_next_redirect_url, complete_signup,
                    get_login_redirect_url, perform_login,
                    passthrough_next_redirect_url,
                    sync_user_email_addresses)
from allauth.account.forms import AddEmailForm, ChangePasswordForm
from allauth.account.forms import ResetPasswordKeyForm
from allauth.account.forms import ResetPasswordForm, SetPasswordForm, SignupForm
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.views import RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, CloseableSignupMixin

from allauth.account import signals
from allauth.account import app_settings

from soulightrd.apps.app_helper import get_user_login_object, get_template_path
from soulightrd.apps.auth.forms import CustomSignupForm, CustomSocialSignupForm, CustomResetPasswordForm, CustomLoginForm

from allauth.account.adapter import get_adapter as get_account_adapter

from allauth.socialaccount import helpers
from allauth.socialaccount import providers
from allauth.socialaccount.adapter import get_adapter as get_social_adapter
from allauth.socialaccount.models import (SocialLogin,
                                          SocialToken)
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.helpers import render_authentication_error

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from allauth.socialaccount.providers.facebook.forms import FacebookConnectForm
from allauth.socialaccount.providers.facebook.provider import FacebookProvider

import logging, requests

User = get_user_model()

logger = logging.getLogger(__name__)

APP_NAME = "auth"


def resend_confirm_email(request):
    user_login = get_user_login_object(request)
    email = user_login.email
    request.session['is_show_request_message'] = True
    try:
        email_address = EmailAddress.objects.get(
                user=request.user,
                email=email,
            )
        get_account_adapter().add_message(request,
                                    messages.INFO,
                                    'account/messages/'
                                    'email_confirmation_sent.txt',
                                    {'email': email})
        email_address.send_confirmation(request)
        return HttpResponseRedirect("/?action=resend_confirm_email&result=success")
    except EmailAddress.DoesNotExist:
        return HttpResponseRedirect("/?action=resend_confirm_email&result=error")


class LoginView(RedirectAuthenticatedUserMixin,
                AjaxCapableProcessFormViewMixin,
                FormView):
    form_class = CustomLoginForm
    success_url = None
    redirect_field_name = "next"

    def form_valid(self, form):
        success_url = self.get_success_url()
        return form.login(self.request, redirect_url=success_url)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ret.update({"app_name": APP_NAME,
                    "signup_url": signup_url,
                    "site": Site.objects.get_current(),
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"login",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

login = LoginView.as_view()


class SignupView(RedirectAuthenticatedUserMixin, CloseableSignupMixin,
                 FormView):
    form_class = CustomSignupForm
    redirect_field_name = "next"
    success_url = "/?action=signup&result=success"

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def form_valid(self, form):
        user = form.save(self.request)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        form.fields["email"].initial = self.request.session \
            .get('account_verified_email', None)
        ret = super(SignupView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"app_name": APP_NAME,
                    "login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"signup",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

signup = SignupView.as_view()


class ConfirmEmailView(TemplateResponseMixin, View):

    def get_template_names(self):
        if self.request.method == 'POST':
            return ["account/email_confirmed.html"]
        else:
            return ["account/email_confirm.html"]

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if app_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        get_account_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/email_confirmed.txt',
                                  {'email': confirmation.email_address.email})
        resp = self.login_on_confirm(confirmation)
        if resp:
            return resp
        # Don't -- allauth doesn't touch is_active so that sys admin can
        # use it to block users et al
        #
        # user = confirmation.email_address.user
        # user.is_active = True
        # user.save()
        redirect_url = self.get_redirect_url()
        self.request.session['is_show_request_message'] = True
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)

    def login_on_confirm(self, confirmation):
        """
        Simply logging in the user may become a security issue. If you
        do not take proper care (e.g. don't purge used email
        confirmations), a malicious person that got hold of the link
        will be able to login over and over again and the user is
        unable to do anything about it. Even restoring his own mailbox
        security will not help, as the links will still work. For
        password reset this is different, this mechanism works only as
        long as the attacker has access to the mailbox. If he no
        longer has access he cannot issue a password request and
        intercept it. Furthermore, all places where the links are
        listed (log files, but even Google Analytics) all of a sudden
        need to be secured. Purging the email confirmation once
        confirmed changes the behavior -- users will not be able to
        repeatedly confirm (in case they forgot that they already
        clicked the mail).

        All in all, opted for storing the user that is in the process
        of signing up in the session to avoid all of the above.  This
        may not 100% work in case the user closes the browser (and the
        session gets lost), but at least we're secure.
        """
        user_pk = self.request.session.pop('account_user', None)
        user = confirmation.email_address.user
        if user_pk == user.pk and self.request.user.is_anonymous():
            return perform_login(self.request,
                                 user,
                                 app_settings.EmailVerificationMethod.NONE)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        return ctx

    def get_redirect_url(self):
        return get_account_adapter().get_email_confirmation_redirect_url(self.request)

confirm_email = ConfirmEmailView.as_view()


class PasswordChangeView(FormView):
    form_class = ChangePasswordForm
    success_url = "/?action=change_password&result=success"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        request.session['is_show_request_message'] = True
        return super(PasswordChangeView, self).dispatch(request, *args,
                                                        **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        get_account_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/password_changed.txt')
        signals.password_changed.send(sender=self.request.user.__class__,
                                      request=self.request,
                                      user=self.request.user)
        return super(PasswordChangeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_change_form'] = ret.get('form')
        ret['app_name'] = APP_NAME
        # (end NOTE)
        return ret

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"password_change",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

password_change = login_required(PasswordChangeView.as_view())


class PasswordSetView(FormView):
    form_class = SetPasswordForm
    success_url = "/?action=change_password&result=success"

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_change_password'))
        request.session['is_show_request_message'] = True
        return super(PasswordSetView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordSetView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        get_account_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/password_set.txt')
        signals.password_set.send(sender=self.request.user.__class__,
                                  request=self.request, user=self.request.user)
        return super(PasswordSetView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(PasswordSetView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_set_form'] = ret.get('form')
        ret['app_name'] = APP_NAME
        # (end NOTE)
        return ret

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"password_set",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

password_set = login_required(PasswordSetView.as_view())


class PasswordResetView(FormView):
    form_class = CustomResetPasswordForm
    success_url = reverse_lazy("account_reset_password_done")

    def form_valid(self, form):
        form.save()
        return super(PasswordResetView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(PasswordResetView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_reset_form'] = ret.get('form')
        ret['app_name'] = APP_NAME
        # (end NOTE)
        return ret

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"password_reset",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

password_reset = PasswordResetView.as_view()


class PasswordResetDoneView(TemplateView):
    template_name = "account/password_reset_done.html"

password_reset_done = PasswordResetDoneView.as_view()


class PasswordResetFromKeyView(FormView):
    form_class = ResetPasswordKeyForm
    token_generator = default_token_generator
    success_url = reverse_lazy("account_reset_password_from_key_done")

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"password_reset_from_key",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

    def _get_user(self, uidb36):
        # pull out user
        try:
            uid_int = base36_to_int(uidb36)
        except ValueError:
            raise Http404
        return get_object_or_404(User, id=uid_int)

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.uidb36 = uidb36
        self.key = key
        self.reset_user = self._get_user(uidb36)
        if not self.token_generator.check_token(self.reset_user, key):
            return self._response_bad_token(request, uidb36, key, **kwargs)
        else:
            return super(PasswordResetFromKeyView, self).dispatch(request,
                                                                  uidb36,
                                                                  key,
                                                                  **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordResetFromKeyView, self).get_form_kwargs()
        kwargs["user"] = self.reset_user
        kwargs["temp_key"] = self.key
        return kwargs

    def form_valid(self, form):
        form.save()
        get_account_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/password_changed.txt')
        signals.password_reset.send(sender=self.reset_user.__class__,
                                    request=self.request,
                                    user=self.reset_user)
        return super(PasswordResetFromKeyView, self).form_valid(form)

    def _response_bad_token(self, request, uidb36, key, **kwargs):
        return self.render_to_response(self.get_context_data(token_fail=True))

password_reset_from_key = PasswordResetFromKeyView.as_view()


class PasswordResetFromKeyDoneView(TemplateView):
    def get(self, request):
        request.session['is_show_request_message'] = True
        return HttpResponseRedirect(reverse('account_login') + "?action=reset_password&result=success")

password_reset_from_key_done = PasswordResetFromKeyDoneView.as_view()


class LogoutView(TemplateResponseMixin, View):

    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if app_settings.LOGOUT_ON_GET:
            return self.post(*args, **kwargs)
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated():
            self.logout()
        return redirect(url)

    def logout(self):
        get_account_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/logged_out.txt')
        auth_logout(self.request)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ctx.update({
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": redirect_field_value})
        return ctx

    def get_redirect_url(self):
        return (get_next_redirect_url(self.request,
                                      self.redirect_field_name)
                or get_account_adapter().get_logout_redirect_url(self.request))

logout = LogoutView.as_view()


class AccountInactiveView(TemplateView):

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"account_inactive",RequestContext(self.request)['flavour'],'/account/')
        return [template_path]

account_inactive = AccountInactiveView.as_view()


class SocialSignupView(RedirectAuthenticatedUserMixin, CloseableSignupMixin,
                 FormView):
    form_class = CustomSocialSignupForm

    def dispatch(self, request, *args, **kwargs):
        self.sociallogin = SocialLogin \
            .deserialize(request.session.get('socialaccount_sociallogin'))
        if not self.sociallogin:
            return HttpResponseRedirect(reverse('account_login'))
        return super(SocialSignupView, self).dispatch(request, *args, **kwargs)

    def is_open(self):
        return get_social_adapter().is_open_for_signup(self.request,
                                                self.sociallogin)

    def get_form_kwargs(self):
        ret = super(SocialSignupView, self).get_form_kwargs()
        ret['sociallogin'] = self.sociallogin
        return ret

    def form_valid(self, form):
        form.save(self.request)
        return helpers.complete_social_signup(self.request,
                                              self.sociallogin)

    def get_context_data(self, **kwargs):
        ret = super(SocialSignupView, self).get_context_data(**kwargs)
        ret.update(dict(site=Site.objects.get_current(),
                        account=self.sociallogin.account))
        return ret

    def get_authenticated_redirect_url(self):
        return "/"

    def get_template_names(self):
        template_path = get_template_path(APP_NAME,"signup",RequestContext(self.request)['flavour'],'/socialaccount/')
        return [template_path]

social_signup = SocialSignupView.as_view()


class LoginCancelledView(TemplateView):
    def get(self, request):
        return HttpResponseRedirect(reverse('account_login'))

login_cancelled = LoginCancelledView.as_view()

class LoginErrorView(View):
    def get(self, request):
        request.session['is_show_request_message'] = True
        return HttpResponseRedirect(reverse('account_login') + "?action=social_login&result=error")

login_error = LoginErrorView.as_view()


def fb_complete_login(request, app, token):
    resp = requests.get('https://graph.facebook.com/me',
                        params={'access_token': token.token})
    resp.raise_for_status()
    extra_data = resp.json()
    login = providers.registry \
        .by_id(FacebookProvider.id) \
        .sociallogin_from_response(request, extra_data)
    return login


class FacebookOAuth2Adapter(OAuth2Adapter):
    provider_id = FacebookProvider.id

    authorize_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    expires_in_key = 'expires'

    def complete_login(self, request, app, access_token, **kwargs):
        return fb_complete_login(request, app, access_token)


oauth2_login = OAuth2LoginView.adapter_view(FacebookOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FacebookOAuth2Adapter)


def login_by_token(request):
    ret = None
    if request.method == 'POST':
        form = FacebookConnectForm(request.POST)
        if form.is_valid():
            try:
                app = providers.registry.by_id(FacebookProvider.id) \
                    .get_app(request)
                access_token = form.cleaned_data['access_token']
                token = SocialToken(app=app,
                                    token=access_token)
                login = fb_complete_login(request, app, token)
                login.token = token
                login.state = SocialLogin.state_from_request(request)
                ret = complete_social_login(request, login)
            except requests.RequestException:
                logger.exception('Error accessing FB user profile')
    if not ret:
        request.session['is_show_request_message'] = True
        return HttpResponseRedirect(reverse('account_login') + "?action=social_login&result=error")
    return ret


def channel(request):
    provider = providers.registry.by_id(FacebookProvider.id)
    locale = provider.get_locale_for_request(request)
    response = render(request, 'facebook/channel.html',
                      {'facebook_jssdk_locale': locale})
    cache_expire = 60 * 60 * 24 * 365
    patch_response_headers(response, cache_expire)
    response['Pragma'] = 'Public'
    return response
