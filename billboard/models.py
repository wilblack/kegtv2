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
        help_text="This is the position of the beer in the board grid. 1 is at the top of the stack.")
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
    nickname = models.CharField(max_length=45, 
                                help_text="This is a descriptive name that you can remember.")
    name = models.CharField(max_length=45, 
                            help_text="This is the technical name")
    width = models.IntegerField(default=785, 
                                help_text="Width in pixels of the display")
    aspect_ratio = models.FloatField(default=1.333, 
                                     help_text="The ascpect ratio in decimal form. For instance 4:3 would be 1.333") 
    
    def __unicode__(self):
        return "%s - (%s)" %(self.nickname, self.name)
    
    @property
    def json(self):
        return {'nickname':self.nickname,
                'name':self.name,
                'width':self.width,
                'aspect_ratio':self.aspect_ratio,
                }
        
class Ad(models.Model):
    name = models.CharField(max_length=45)
    template = models.CharField(max_length=45, blank=True)
    menu = models.ForeignKey(Menu)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    