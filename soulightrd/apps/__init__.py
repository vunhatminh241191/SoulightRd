from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.template import RequestContext
from django.http import HttpResponseRedirect

from soulightrd.apps.app_helper import get_template_path

class AppBaseView(TemplateResponseMixin,ContextMixin):
	sub_path = "/page/"
	fail_url = None

	def get_context_data(self, **kwargs):
		context = super(AppBaseView, self).get_context_data(**kwargs)
		context['app_name'] = self.app_name
		return context

	def get_template_names(self):	
		return [get_template_path(self.app_name,self.template_name,RequestContext(self.request)['flavour'],self.sub_path)]

	def handle_fail_request(self):
		if self.fail_url == None:
			raise Exception("Fail to handle request. Redirect to 500 error page")
		else:
			return HttpResponseRedirect(self.fail_url)