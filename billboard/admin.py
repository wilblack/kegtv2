from django.contrib import admin
from billboard.models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['beer', 'menu', 'position']
    list_filter = ['menu']
    

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)