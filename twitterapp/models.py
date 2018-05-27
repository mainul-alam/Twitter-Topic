from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialToken
import twitter


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, )

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, )
    comment = models.CharField(max_length=250)
    tweet_id = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_comment(self):
        if self.tweet_id:      # how ?
            tweet = TwitterApi.readTweet(self.user, self.tweet_id)
            return 'TWEET: ' + tweet.text
        else:
            return 'INTERNAL: ' + self.comment


class TwitterApi:
    def getTwitterApi(user):   # what is user ?
        tokens = SocialToken.objects.get(account__user=user) #what objects.get means ?
        api = twitter.Api(consumer_key='2Be4eBRrGH0KlBGmYNVwKP2Az',
                          consumer_secret='QKGluMGNf3fABBiP4uvAiwaR2K5pJVtKzzksuYtk6kbmjNfKOP',
                          access_token_key=tokens.token,
                          access_token_secret=tokens.token_secret)
        return api

    def postTweet(user, tweet):
        api = TwitterApi.getTwitterApi(user)
        return api.PostUpdate(tweet)

    def readTweet(user, tweet_id):
        api = TwitterApi.getTwitterApi(user)
        tweet = api.GetStatus(tweet_id)
        return tweet

    def getTweetsByUser(user):
        tweets = []

        try:
            api = TwitterApi.getTwitterApi(user)
            user_id = api.VerifyCredentials().id       # what is this doing ?
            latest = api.GetUserTimeline(user_id)
            for tweet in latest:                     # how is this working ?
                status = tweet.text
                tweet_date = tweet.created_at
                tweets.append({'status': status, 'date': tweet_date})
        except:
            tweets.append({'status': 'its not working', 'date': 'about 10 minutes ago'})
        return tweets
