from django.contrib import admin
from billboard.models import Menu, MenuItem, DisplaySettings

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'footer', 'display_settings','modified', 'entered']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['beer', 'menu', 'position']
    list_filter = ['menu']
    
class DisplaySettingsAdmin(admin.ModelAdmin):
    list_display=['id' ,'nickname', 'name', 'width', 'aspect_ratio']
    
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(DisplaySettings, DisplaySettingsAdmin)