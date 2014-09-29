from haystack import indexes

from django.contrib.auth.models import User
from django.db.models import Q

from soulightrd.apps.main.models import Project, Organization, UserProfile


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='organization')
    content = indexes.CharField(model_attr="name")

    def get_model(self):
        return Project

  	def index_queryset(self, using=None):
		return self.get_model().objects.all()	

   
class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	content = indexes.CharField(model_attr="name")
	
	def get_model(self):
		return Activity

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(is_verified=True)


class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	content = indexes.CharField(model_attr="get_user_fullname")

	def get_model(self):
		return UserProfile

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

