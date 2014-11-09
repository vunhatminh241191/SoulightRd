from django.contrib.auth.models import User
from django.conf.urls import *

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from views import MainSearchView, get_city_autocomplete_data

from soulightrd.apps.main.models import Project, Organization

mainSQS = SearchQuerySet().models(Project,Organization)

urlpatterns = patterns('haystack.views',

    # url(r'^autocomplete/$', get_all_autocomplete_data),
    url(r'^autocomplete/city/$', get_city_autocomplete_data),

    url(r'^$',search_view_factory(
                    view_class=MainSearchView,
                    searchqueryset=mainSQS,
                    form_class=ModelSearchForm
                ), name="main_search")
)