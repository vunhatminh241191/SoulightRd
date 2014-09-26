from django.contrib.auth.models import User
from django.conf.urls import *

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

urlpatterns = patterns('haystack.views',

)