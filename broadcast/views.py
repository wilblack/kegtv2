import logging
import twitter
import ttp
import datetime as dt

from json import dumps as json

from django.http import HttpResponse
tweet_parser = ttp.Parser()

from broadcast.models import Tweet

def twitter_get(request, menu_id):
    """
    And API to return the latest @barleyboard twitter mentions. 
    This is available by going to 
    /broadcast/twitter/get/1/
    
    Returns a list of tweets as text.
    """
    get = request.GET
        
    #TODO Use menu id to get brewpub, and then their twitter account info
    twitter_user = "barleyboard"
    tweets = []
    api = twitter_authenticate()
    
    try:
        mentions = api.GetMentions()
    except (twitter.TwitterError, URLError), e:
        logging.getLogger(__name__).error(str(e))
        context[asvar] = cache.get(cache_key, [])
        return ""

    # This is to exclude users that you don't want.
    
    #tweets =  ["%s - %s" %(status.GetUser().screen_name, status.text)
    #            for status in mentions]
    for status in mentions: 
        user = status.GetUser().screen_name
        text = "%s" %(status.text.split(" ", 1)[1])
        twitter_id = status.id
        created_at = status.created_at_in_seconds
        
        entry = {'text':text,
                 'user':user, 
                 'created_at':created_at,
                 'twitter_id':twitter_id,
                 }
        tweet, created = Tweet.objects.get_or_create(twitter_id = twitter_id)
        if created:
            tweet.user = user
            tweet.created_at = created_at
            tweet.text = text
            tweet.save()
            
        tweets.append(entry)
        tweets.reverse() # This should put the oldest ones first.
        
    return HttpResponse(json(tweets))

def twitter_authenticate():
    
    consumer_key='6srqbNL9e8pFzvvdRNMaAg'
    consumer_secret='3Suzh16ytevzdi2IDcz30F258BMkna1yM2WcUs03s8'
    
    # The oAuth access token key value you retrieved
    # from running get_access_token.py.  
    access_token_key='422788502-NoB2TbkMT5AwaL6ezcW2mMnarmKPJJAzx2Np1X8F'    
    access_token_secret='dysmsrorJvDmrMoQoMQEZSJXy4i2UmwmypFvhXCxyQ'
    
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret
                      )
    
    return api
    