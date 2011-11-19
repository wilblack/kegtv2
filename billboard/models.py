from django.db import models
from beers.models import Beer

class Menu(models.Model):
    title = models.CharField(max_length=45)
    footer = models.CharField(max_length=100, blank=True)
    display_settings = models.ForeignKey('DisplaySettings') 
    entered = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return self.title   
    

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    beer = models.ForeignKey(Beer)
    menu = models.ForeignKey(Menu, blank=True, null=True)
    position = models.CharField(max_length=45, blank=True,
        help_text="This is the row column position of the beer in the board grid. It should look somthing like 2-4.")
    slogan = models.TextField(blank=True,
            help_text="A short phrase that will show up in the billboard.")
    
    def __unicode__(self):
        return self.beer.name
    
    def json(self):
        beer_json = self.beer.json()
    
        beer_json.update({'id':self.id,
                          'slogan':self.slogan,
                          'position':self.position,
                          'menu_id':self.menu_id,
                        })
        return beer_json
    
    
class DisplaySettings(models.Model):
    name = models.CharField(max_length=45)
    WIDTH = models.IntegerField(default=785, help_text="Width in pixels of the display")
    NROWS = models.IntegerField(default=4)
    NCOLS = models.IntegerField(default=3)
    
    MENU_TITLE_HEIGHT = models.CharField(max_length=10, default="6%")
    MENU_GRID_HEIGHT = models.CharField(max_length=10, default="86%")
    MENU_GRID_WIDTH = models.CharField(max_length=10, default="99.9%")
    COL_HEIGHT = models.CharField(max_length=10, default="99%")
    COL_WIDTH = models.CharField(max_length=10, default="32.9%")
    GRID_CELL_HEIGHT = models.CharField(max_length=10, default="24%")
    GRID_CELL_WIDTH = models.CharField(max_length=10, default="100%")
    MENU_FOOTER_HEIGHT = models.CharField(max_length=10, default="5%")
    
    def __unicode__(self):
        return self.name
    