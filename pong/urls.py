from django.conf.urls.defaults import *

urlpatterns = patterns(
    'pong.views',
    url(r'menu/(?P<menu_id>\d+)/?$','pong', name="ping"),
)