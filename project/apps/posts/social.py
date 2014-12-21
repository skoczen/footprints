from facepy import GraphAPI
import tweepy

from django.conf import settings
from django.core.urlresolvers import reverse


def twitter_auth():
    twitter_callback_url = "%s%s" % (settings.BASE_URL, reverse("posts:twitter_auth_finish"))
    return tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET, twitter_callback_url)

def authorized_tweepy_api(author):
    auth = twitter_auth()
    auth.set_access_token(author.twitter_api_key, author.twitter_api_secret)

    return tweepy.API(auth)


def facebook_auth():
    facebook_callback_url = "%s%s" % (settings.BASE_URL, reverse("posts:facebook_auth_finish"))
    return  OAuth2(settings.FACEBOOK_APP_KEY, settings.FACEBOOK_APP_SECRET, 
                "https://www.facebook.com/",
                facebook_callback_url,
                "dialog/oauth", "oauth/access_token"
            )

def authorized_facebook_api(author):
    return GraphAPI(author.facebook_api_key)
