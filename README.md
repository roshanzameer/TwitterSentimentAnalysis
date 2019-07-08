# Real-time Twitter Sentiment Analysis and Storage

Analyse the sentiments of tweets in Real-time stream through Kafka and store the processed tweets to database

Overview:

1. The Module connects to Twitter Search API and Stream API to fetch tweets for a given hashtag.
2. The fetched tweets are procesed, sentiment analysis is done and the processed tweets along with the sentiment tags is flushed to a Kafka     topic
3. The Consumer modules connects to the Kafka topic and fetches the messages.
4. The messages are then written to a Postgres Database


Instructions:

1. The Docker-Compose script when composed, brings up a PostgreSQL server, PgAdmin Client, Zookeper, and Kafka Server.

2. The Port address and IP Address of the docker container interfaces is to be set accordingly.

3. If the services are already present and running, the said, service can be commented in the compose script.

        sudo docker-compose up 
        
4. Once the PostgreSQL server is up, export the Schema from the dump file twitter_db_schema.sql. 
        
        cat twitter_db_schema.sql | docker exec -i 'your-db-container' psql -U postgres
        
5. Ensure that the Table TwitterData is created.
    
6. Once the containers are live, the required python packages for the project can be installed from the requirements.txt file.
    
        pip install -r requirements.txt
    
7. Navigate to the Consumer directory and run the Kafka Consumer Instance. The consumer instance also writes the messages to the Database. Make sure the connection strings and the Kafka Bootstrap Server addresses are right.

        python consumer.py
  
8. The Consumer instance after starting, waits for the messages to stream through the 'twitter' topic.

9. Now navigate to the Producer directory and enter the credentials for your Twitter APP in the Credentials.py file.

10. Make sure the IP address of the Kafka Bootstrap server is right in the Kafka_producer.py module.

11. Now navigate to the Producer directory and run the 'tweet_producer' module.

        python tweet_producer.py
        
12. The tweet_producer.py module connects to the Twitter Search API and fetch tweets for the given time range. Modify the arguments in the get_tweets function to the desired Time Range and Hashtag

13. The realtime_tweet.py module connects to Twitter's Stream API to fetch tweets in Real-Time. Modify the 'track' argument in main() method to the desired hashtag.

14. The module first fetches the older tweets for the given time range and then calls the LiveListener class to fetch tweets in realtime. 

15. Everytime a tweet is fetched, the Sentiment Analysis is done. Vader package is used in this case.

16. For every tweet, the Date of creation, Tweet Text, and Sentiment detail is written to the Database.

