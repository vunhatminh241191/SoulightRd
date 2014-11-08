from django.conf.urls import *

from . import views
from . import forms

urlpatterns = patterns("",
   url(r"^create/$", views.create_organization ,{'form_class': forms.OrganizationSignUpForm}
   	,name="create_organization"),
   url(r"^delete/$","delete_organization",name="delete_organization"),
   url(r"^(?P<organization_unique_id>\w+)/edit/$","edit_organization",name="edit_organization"),
   url(r"^(?P<organization_unique_id>\w+)/$",views.organization_main,name="organization_main"),
   url(r"^(?P<organization_unique_id>\w+)/projects/$", views.list_projects, name="organization_list_projects"),

)
