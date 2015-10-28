"""
Stream live tweets using the twitter API and tweepy. Streams are stored in a mongodb database.
Set filter keywords at bottom.
Stop by interrupting (Ctrl-C) or setting max_tweets

Requires the extra libraries:
pymongo
tweepy

The data is stored in pymongo database:
tweet_db
Collection:
TweetsReceived
"""
import pymongo
import sys
import tweepy

"""
create listener object that processes the stream of tweets of tweepy.StreamListener
created mongodb called:
tweet_db.TweetsReceived
"""
class TweetsStreamListener(tweepy.StreamListener):

    def __init__(self, api, max):
                
        #override constructor to init mongodb and the tweepy.StreamListener automatically, 
        #so no need to do it before
        super(tweepy.StreamListener, self).__init__()
        try:
            self.db = pymongo.MongoClient().tweet_db
            print "Connected to MongoDB"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB, reason: %s" % e 
        self.api = api
        self.max_tweets = max
        self.counter = 0
    #handle all the returns of the stream
    def on_connect(self):
        print "Connected to a tweet stream!"
    #if the listener finds a tweet, save to mongodb
    def on_status(self, status):
        print str(status.created_at) +": " +status.text.encode("utf-8")
        tweet ={}
        tweet['text'] = status.text
        tweet['created_at'] = status.created_at
        tweet['geo'] = status.geo
        tweet['source'] = status.source
        #insert into collection TweetsReceived
        self.db.TweetsReceived.insert(tweet)
        self.counter += 1
        if self.max_tweets and self.counter > self.max_tweets:
            print "Set limit of %s reached" % self.max_tweets
            return False
    def on_error(self, status_code):
        print >> sys.stderr, 'Problem with stream: ', status_code
        #continue
        return True 
    def on_timeout(self):
        print >> sys.stderr, 'currently timed out..'
        return True 
    def on_limit(self, track):
        print "-!- Collection limit hit. {0} matching tweets not delivered".format(track)
    #if disconnected by twitter, report and stop
    def on_disconnect(self, notice):
        print "Disconnected by twitter. Reason: {0}".format(notice['reason'])
        return False

if __name__ == "__main__":
    """do twitter authentication here"""
    #At http://dev.twitter.com sign up for new application (need twitter account)
    consumer_key="PERSONAL, GET FROM TWITTER"
    consumer_secret="PERSONAL, GET FROM TWITTER"
    # get by https://dev.twitter.com/oauth/overview/application-owner-access-tokens
    access_token="PERSONAL, GET FROM TWITTER"
    access_token_secret="PERSONAL, GET FROM TWITTER"
    #get authorization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    """set max tweet n (keep empty if continously, then stop with ctrl+c)"""
    max_tweets = 100
    #set up the listener and pass in the api and max, db will be created in this object"""
    listener = tweepy.streaming.Stream(auth, TweetsStreamListener(api, max_tweets))
    """Set filter about what you want the stream to pick up."""
    listener.filter(track=["susi", "manhattan" ], languages=["en"])