from django.db import models

# Create your models here.

class Beer(models.Model):
    name = models.CharField(max_length=100)
    brewery = models.ForeignKey('Brewery')
    beer_type = models.ForeignKey('BeerType')
    abv = models.FloatField(blank=True, null=True)
    about = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    def json(self):
        
        return {'beer_id':self.id,
                'name':self.name,
                'brewery':self.brewery.name,
                'brewery_city':self.brewery.city,
                'brewery_state':self.brewery.state,
                'beer_type':self.beer_type.name,
                'abv':self.abv,
                'color1':self.beer_type.color1,
                'color2':self.beer_type.color2,
                'color3':self.beer_type.color3,
                
                }
    
class BeerType(models.Model):
    name = models.CharField(max_length=45)
    about = models.TextField(blank=True)    
    color1 = models.CharField(max_length=7,
                             default="#CC9900",
                             help_text="This is the menu background color for this beer type.")
    
    color2 = models.CharField(max_length=7,
                             default="#333399",
                             help_text="Color used to determine this type of beer.")
    
    color3 = models.CharField(max_length=7,
                             default="#006666",
                             help_text="Color used to determine this type of beer.")
    
    
    def __unicode__(self):
        return self.name
    
class Brewery(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    
    def __unicode__(self):
        return self.name