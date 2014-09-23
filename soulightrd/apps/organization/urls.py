from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('soulightrd.apps.organization.views',
   url(r'^create/$','create_organization',name="create_organization"),
   url(r"^delete/$","delete_organization",name="delete_organization"),
   url(r"^(?P<organization_unique_id>\w+)/edit/$","edit_organization",name="edit_organization"),
   url(r"^(?P<organization_unique_id>\w+)/$","main_page",name="organization_main"),

)
