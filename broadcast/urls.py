from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'broadcast.views',
    
    url(r'twitter/get/(?P<menu_id>\d+)/$', 'twitter_get', name="twitter_get"),    
)