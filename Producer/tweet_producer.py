"""

This module connects to Twitter Developer API to stream Tweets.

TwitterClient():
1. The TwitterClient() class is a generic class which connects to twitter Search API and fetches tweets for a specified Hashtag and flushes
the tweets, date, sentiment to a Kafka topic.
2. The sentiment analysis is done by the Vader package.


"""

import json
import tweepy
from tweepy import OAuthHandler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from credentials import consumer_key, consumer_secret
from credentials import access_token, access_secret
from kafka_producer import KafkaStreamer
from realtime_tweets import LiveListener

auth = OAuthHandler(consumer_key, consumer_secret)
# set access token and secret
auth.set_access_token(access_token, access_secret)
# create tweepy API object to fetch tweets
api = tweepy.API(auth)

class TwitterClient(object):

    """
    Generic Twitter Class for sentiment analysis.
    """

    def get_tweet_sentiment(self, tweet):

        """
        Utility function to classify sentiment of passed tweet
        using VaderSentiment Analyzer
        """

        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(tweet)
        # set sentiment
        if vs['compound'] >= 0.05:
            return 'positive'
        elif -0.5 < vs['compound'] < 0.05:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, kafka_obj):

        """
        Main function to fetch tweets and parse them.
        """

        try:

            # call twitter api to fetch tweets
            # for tweet in api.search('#machinelearning', count=5):

            for tweet in tweepy.Cursor(api.search, q='#machinelearning', since='2019-07-05').items():

                # empty dictionary to store required params of a tweet
                parsed_tweet = dict()
                parsed_tweet['text'] = tweet.text
                parsed_tweet['date'] = str(tweet.created_at)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                print('Search API', parsed_tweet)

                #Pushing all the tweets to the Kafka Topic

                kafka_producer = kafka_obj.producer_instance()
                kafka_obj.publish_urls(kafka_producer, 'twitter', 'tweet', json.dumps(parsed_tweet))

        except Exception as e:
            print(e)

def main():

    #creating object of KafkaStreamer Class
    kafka_obj = KafkaStreamer()

    # creating object of TwitterClient Class
    tw_obj = TwitterClient()

    # calling function to get tweets
    tw_obj.get_tweets(kafka_obj)

    #calling listener function for realtime streaming
    streamingAPI = tweepy.streaming.Stream(auth, LiveListener(kafka_obj=kafka_obj, tw_obj=tw_obj))
    streamingAPI.filter(track=['#machinelearning'])


if __name__ == "__main__":

    # calling main function
    main()
