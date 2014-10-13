from haystack import indexes

from django.contrib.auth.models import User
from django.db.models import Q

from cities_light.models import City

from soulightrd.apps.main.models import Project, Organization, UserProfile


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='organization')
    content = indexes.CharField(model_attr="title")

    def get_model(self):
        return Project

  	def index_queryset(self, using=None):
		return self.get_model().objects.all()	

   
class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	content = indexes.CharField(model_attr="name")
	
	def get_model(self):
		return Organization

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(is_verified=True)

class CityIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	content = indexes.CharField(model_attr="search_names")

	def get_model(self):
		return City

	def index_queryset(self,using=None):
		return self.get_model().objects.filter(country__code2="VN")

class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	content = indexes.CharField(model_attr="get_user_fullname")

	def get_model(self):
		return UserProfile

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

