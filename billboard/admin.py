from django.contrib import admin
from broadcast.models import Tweet 

class TweetAdmin(admin.ModelAdmin):
    list_display = ['twitter_id', 'user', 'created_at', 'text', 'entered']

    
admin.site.register(Tweet, TweetAdmin)