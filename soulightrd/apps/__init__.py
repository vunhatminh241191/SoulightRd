from django.views.generic.base import ContextMixin
from django.template import RequestContext

from soulightrd.apps.app_helper import get_template_path

class AppBaseView(ContextMixin,TemplateResponseMixin):
	sub_path = "/page/"

	def get_context_data(self, **kwargs):
		context = super(ContextBaseView, self).get_context_data(**kwargs)
		context['app_name'] = self.app_name
		return context

	def get_template_names(self):		
		return [get_template_path(self.app_name,self.template_name,RequestContext(self.request)['flavour']),self.sub_path]
