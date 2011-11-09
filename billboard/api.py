# myapp/api.py
from tastypie import fields
from tastypie.resources import ModelResource
from billboard.models import MenuItem, Menu

class MenuItemResource(ModelResource):
    class Meta:
        queryset = MenuItem.objects.all()
        resource_name = 'menuitem'
        
        
class MenuResource(ModelResource):
    items = fields.ToManyField(MenuItemResource, 'menuitem_set', related_name='menuitem')
    
    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'