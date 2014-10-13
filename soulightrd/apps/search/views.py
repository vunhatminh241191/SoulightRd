from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

from haystack.views import SearchView
from haystack.query import SearchQuerySet

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "search"

class MainSearchView(SearchView):

	def create_response(self):
		(paginator, page) = self.build_page()

		context = {
			'query': self.query,
			'form': self.form,
			'page': page,
			'paginator': paginator,
			'suggestion': None,
			"app_name": APP_NAME
		}

		if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
			context['suggestion'] = self.form.get_suggestion()

		project_results = []
		organization_results = []
		for result in self.results:
			if "project" in result.model_name:
				project_results.append(result)
			if "organization" in result.model_name:
				organization_results.append(result)

		context['project_results'] = project_results
		context['organization_results'] = organization_results
		
		context.update(self.extra_context())
		template = get_template_path(APP_NAME,"main_search",context_instance['flavour'])
		return render_to_response(template, context, context_instance=self.context_class(self.request))

