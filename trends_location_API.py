"""
This API returns the trending hashtag and location detail of the country with most tweets along with the count

"""

from flask import Flask, request
import logging
from flask_cors import CORS
import psycopg2
app = Flask(__name__)
CORS(app)
import json

@app.route('/data', methods=['GET'])

def CallAll():
    info = dict()
    country, hashtag = fetch_database()

    info['Max_tweet_country'] = get_max_count(country)
    info['trending_hashtag'] = get_max_count(hashtag)

    return json.dumps(info)

def fetch_database():
    connection = psycopg2.connect(user='postgres', host='172.16.238.10', port='5432', password='Qwerty1234',
                                  database='postgres')
    cursor = connection.cursor()
    countries = []
    hashtags = []
    try:

        cursor.execute('SELECT location, hashtags from public."TwitterData"')
        data_all = cursor.fetchall()
        
        #returning both location and hashtag data from the database
        for data in data_all:
            countries.append(data[0])
            hashtags.append(data[1])

        return countries, hashtags

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


def get_max_count(all_list):
    unique_data = list(set(all_list))
    max_count = 0
    max_count_data = ''
    
    #iterating over the list and reducing to the number of occurences
    for data in unique_data:
        
        #ignoring empty data
        if data:
            temp_dict = dict()
            temp_dict[data] = all_list.count(data)

            if temp_dict[data] > max_count:
                max_count = temp_dict[data]

                max_count_data = temp_dict

    return max_count_data



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7777)
