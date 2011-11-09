from django.db import models
from beers.models import Beer

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=45)
    
    def __unicode__(self):
        return self.title   
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    beer = models.ForeignKey(Beer)
    menu = models.ForeignKey(Menu, blank=True, null=True)
    position = models.CharField(max_length=45, blank=True,
        help_text="This is the row column position of the beer in the board grid. It should look somthing like 2-4.")
    slogan = models.TextField(blank=True,
            help_text="A short phrase that will show up in the billbord.")
    
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