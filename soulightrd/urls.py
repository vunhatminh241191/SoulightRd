from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf import settings

from soulightrd.apps.main.views import error_page

from djrill import DjrillAdminSite

from soulightrd import settings as soulightrd_settings

dajaxice_autodiscover()
admin.site = DjrillAdminSite()
admin.autodiscover()

urlpatterns = patterns('',
    # Admin URL
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include("soulightrd.apps.auth.urls")),

    # Haystack app URL
    url(r'^search/', include("soulightrd.apps.search.urls")),

    # soulightrd URL
    url(r'^$', include('soulightrd.apps.main.urls')),
    url(r'^settings/$','soulightrd.apps.member.views.settings_page',name="account_settings"),

    url(r'^discover/',include('soulightrd.apps.discover.urls')),
    url(r'^about/',include('soulightrd.apps.about.urls')),
    url(r"^notification/",include("soulightrd.apps.notification.urls")),
    url(r'^messages/',include('soulightrd.apps.message.urls')),
    url(r'^organization/',include('soulightrd.apps.organization.urls')),
    url(r'^project/',include('soulightrd.apps.project.urls')),
    url(r'^people/(?P<username>\w+)/',include('soulightrd.apps.member.urls')),

    # Error page
    url(r'^error/$',error_page),
                    
    # Dajaxice URL
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Media URL
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

    url(r'^i18n/', include('django.conf.urls.i18n')),

)

handler403 = error_page
handler404 = error_page
handler500 = error_page
