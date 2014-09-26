from django.conf.urls import *

urlpatterns = patterns('soulightrd.apps.main.views',
    url(r"^$", "main_page"),
)
