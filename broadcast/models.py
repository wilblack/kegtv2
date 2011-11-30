from django.db import models

# Create your models here.

class Tweet(models.Model):
    twitter_id = models.IntegerField(unique=True)
    text = models.CharField(max_length=145, blank=True)
    created_at = models.IntegerField(blank=True, null=True)
    user = models.CharField(max_length=45,
                            help_text="Twitter user screen name",
                            blank=True)
    
    entered = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    
    
