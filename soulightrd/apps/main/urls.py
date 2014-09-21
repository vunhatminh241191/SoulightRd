from django.conf.urls.defaults import *
from soulightrd import settings

urlpatterns = patterns('soulightrd.apps.main.views',
    url(r"^$", "main_page"),
)
