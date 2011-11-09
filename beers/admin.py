from django.contrib import admin
from beers.models import Beer, Brewery, BeerType

class BeerAdmin(admin.ModelAdmin):
    list_display = ['name', 'brewery', 'beer_type']

class BeerTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'about', 'color1', 'color2', 'color3']
    list_editable = ['color1', 'color2', 'color3']
    
class BreweryAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state']

admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerType, BeerTypeAdmin)
admin.site.register(Brewery, BreweryAdmin)