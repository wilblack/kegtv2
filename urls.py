from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from billboard.api import MenuItemResource, MenuResource


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MenuItemResource())
v1_api.register(MenuResource())

urlpatterns = patterns('',
    # Examples:
    (r'^/?$', direct_to_template ,{"template":"coming_soon.html"} ),
    #url(r'^$', 'kegtv.views.home', name='home'),
    (r'^beers/', include('beers.urls')),
    (r'^billboard/', include('billboard.urls')),
    
    (r'^api/', include(v1_api.urls)),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
