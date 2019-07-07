"""

KafkaStreamer():
1. This class creates an instance of the kafka Producer instance.
2. The instance flushes each tweet to the Topic 'Twitter'
3. The bootstrap server is set to the localhost address. Subject to change depending on the local environment.
4. The kafka-python package is used to connect to the Kafka core services.

"""


from kafka import KafkaProducer

class KafkaStreamer():

    def producer_instance(self):

        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        except Exception as ex:
            print('PRODUCER', ex)

        finally:
            return _producer

    def publish_urls(self, producer_instance, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
            producer_instance.flush()
            print('Message publish successfully')
        except Exception as ex:
            print('publish_urls', ex)
