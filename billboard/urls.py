from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()



urlpatterns = patterns(
    'billboard.views',
    url(r'show/(?P<menu_id>\d+)/$','show', name="menu_show"),
    url(r'edit/(?P<menu_id>\d+)/$','edit', name="menu_edit"),
    url(r'edit/menu_item/(?P<menu_item_id>\d+)/$', 'menu_item_JSON', name="menu_item_edit"),
 
    url(r'menuitem/save/', 'menu_item_save'),
    url(r'$','index', name="billboard_list"),
    
    
)