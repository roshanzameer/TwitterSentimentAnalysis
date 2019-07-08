"""
This module connects to the Kafka topic and fetches the messages.
The fetched messages are parsed into JSON format and written to the Database
"""

import json
from kafka import KafkaConsumer
from time import sleep
import psycopg2

def consumer_instance(topic_name):

    consumer = None
    try:
        while True:
            print('Connecting to Kafka Topic')

            consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest', bootstrap_servers=['localhost:9092'],
                                     api_version=(0, 10))
            for message in consumer:
                try:
                    data = json.loads(message.value.decode('utf-8'))
                    print(data)
                    tweet = data['text']
                    date = data['date']
                    sentiment = data['sentiment']
                    location = data['location']
                    tweet_id = data['tweet_id']
                    retweet_count = data['retweet_count']
                    user = data['user']
                    hashtags = data['hashtags']
                                        
                    #calling the function to insert messages into the Database
                    data_store(date, tweet, sentiment, location, tweet_id, retweet_count, user, hashtags)
                    
                except Exception as e:
                    print('consumer while', e)

    except Exception as ex:
        print('consumer instance', ex)

    finally:
        consumer.close()
        cursor.close()
        connection.close()

def data_store( date, tweet, sentiment):

    try:
        
        #inserting data to the Database
        cursor.execute(
            'INSERT INTO "TwitterData" (id, tweet_id, date, tweets, sentiment, location, retweet_count, user, hashtags)'
            ' VALUES (Default, %s, %s, %s, %s, %s, %s, %s, %s)', (tweet_id, date, tweet, sentiment, location, retweet_count, user, hashtags)
            )
        connection.commit()
        print('Data written to Database')

    except Exception as e:
        print('datastore', e)




if __name__ == '__main__':
    print('Connecting to DB')
    connection = psycopg2.connect(user='postgres', host='172.16.238.10', port='5432', password='Qwerty1234',
                                  database='postgres')
    cursor = connection.cursor()
    print('Connection to DB successful')

    consumer_instance('twitter')
