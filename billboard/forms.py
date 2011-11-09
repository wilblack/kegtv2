from billboard.models import MenuItem
from django.forms import ModelForm

from billboard.models import MenuItem

class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem