from django.conf.urls import *

from . import views
from . import forms

urlpatterns = patterns("",
   url(r"^create/$", views.create_organization, name="create_organization"),
   url(r"^list/$", views.list_organization, name="list_organization"),
   url(r"^(?P<organization_unique_id>\w+)/delete/$", views.delete_organization
   	,name="delete_organization"),
   url(r"^(?P<organization_unique_id>\w+)/edit/$", views.edit_organization
   	,name="edit_organization"),
   url(r"^(?P<organization_unique_id>\w+)/$", views.organization_detail
   	,name="organization_detail"),
   url(r"^(?P<organization_unique_id>\w+)/inviting/$"
   	,views.organization_inviting_member, name="organization_inviting_member"),
   url(r"^(?P<organization_unique_id>\w+)/(?P<user_email>\w+)/$",
   	views.organization_accepting_member, name="organization_accepting_member")
)
