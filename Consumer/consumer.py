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
                    tweet = data['text']
                    date = data['date']
                    sentiment = data['sentiment']
                    print(date, tweet, sentiment)
                    data_store(date, tweet, sentiment)


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
        cursor.execute(
            'INSERT INTO "TwitterData" (id, date, tweets, sentiment)'
            ' VALUES (Default, %s, %s, %s)', (date, tweet, sentiment)
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