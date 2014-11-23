from django.conf.urls import *

from . import views
from . import forms

urlpatterns = patterns("",
   url(r"^create/$", views.create_organization ,{'form_class': forms.OrganizationSignUpForm}
   	,name="create_organization"),
   url(r"^list/$", views.list_organization, name="list_organization"),
   url(r"^delete/$","delete_organization",name="delete_organization"),
   url(r"^(?P<organization_unique_id>\w+)/edit/$", views.edit_organization,
   	{'form_class': forms.OrganizationUpdateForm}, name="edit_organization"),
   url(r"^(?P<organization_unique_id>\w+)/$",views.organization_detail
   	,name="organization_detail"),
)