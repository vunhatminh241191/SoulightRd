from django.conf.urls import *

urlpatterns = patterns('soulightrd.apps.project.views',
   url(r'^create/$','create_project',name="create_project"),
   url(r"^delete/$","delete_project",name="delete_project"),
   url(r"^(?P<project_unique_id>\w+)/edit/$","edit_project",name="edit_project"),
   url(r"^(?P<project_unique_id>\w+)/$","main_page",name="project_main"),

)
