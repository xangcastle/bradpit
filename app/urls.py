from django.conf.urls import url
from .views import *

urlpatterns = [
                       url(r'^$', Index.as_view(), name="app_index"),

                       ]
