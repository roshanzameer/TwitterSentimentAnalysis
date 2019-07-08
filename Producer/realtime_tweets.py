"""
LiveListener():
1. This class connects to Twitter Stream and Filter API.
2. Tweets arriving in real-time are pushed to the Kafka Topic

"""


import tweepy
import json
import csv


class LiveListener(tweepy.StreamListener):

    def __init__(self, kafka_obj, tw_obj):
        self.kafka_obj = kafka_obj
        self.tw_obj = tw_obj
        super(LiveListener, self).__init__()

    def on_connect(self):
        print('<<<<<<<<<<<<<Live Stream starting>>>>>>>>>>>>>>>>>')


    def on_status(self, status):

        # print(status.created_at, status.text.encode('utf-8'))

        parsed_tweet = dict()
        parsed_tweet['text'] = status.text
        parsed_tweet['date'] = str(status.created_at)
        parsed_tweet['sentiment'] = self.tw_obj.get_tweet_sentiment(status.text)
        parsed_tweet['tweet_id'] = status.id_str
        parsed_tweet['location'] = status.user.location
        parsed_tweet['user'] = status.user.screen_name
        parsed_tweet['retweet_count'] = status.retweet_count

        if status.entities.get('hashtags'):
            parsed_tweet['hashtags'] = ', '.join([i['text'] for i in status.entities.get('hashtags')])
        else:
            parsed_tweet['hashtags'] = ''
            
        print('Live Stream', parsed_tweet)
        
        # Flushing the messages to a kafka Topic
        
        kafka_producer = self.kafka_obj.producer_instance()
        self.kafka_obj.publish_urls(kafka_producer, 'twitter', 'tweet', json.dumps(parsed_tweet))
        

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True  # Don't kill the stream
