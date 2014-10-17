from django.conf.urls import *
from views import MainView

urlpatterns = patterns('',
    url(r"^$", MainView.as_view()),
)
