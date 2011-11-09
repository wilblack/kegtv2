from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    'beers.views',
    (r'/$','index'),
)