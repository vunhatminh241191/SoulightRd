from django.conf.urls import *

from . import views
from . import forms

urlpatterns = patterns("",
   url(r'^create/$', views.create_organization ,{'form_class': forms.OrganizationSignUpForm}
   	,name="create_organization"),
   url(r"^delete/$","delete_organization",name="delete_organization"),
   url(r"^(?P<organization_unique_id>\w+)/edit/$","edit_organization",name="edit_organization"),
   url(r"^(?P<organization_unique_id>\w+)/$","main_page",name="organization_main"),

)
