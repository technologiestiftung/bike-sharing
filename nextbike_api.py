import requests 
import json
import pandas as pd
import datetime
import os
# import psycopg2

# TODO: also station information

# request data
URL = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_bn/en/free_bike_status.json"

# sending get request and saving the response as response object 
response = requests.get(url = URL) 

try:
    r = response.json()
    new_positions = pd.DataFrame(index=[datetime.datetime.now()])
    for i in range(len(r['data']['bikes'])):
        new_positions[r['data']['bikes'][i]['bike_id']] = str(r['data']['bikes'][i]['lat']) + ', ' + str(r['data']['bikes'][i]['lon'])
	
    if os.path.isfile('./nextBikeData.csv'):

	    old_positions = pd.read_csv('nextBikeData.csv', index_col=0)
	    new_positions = pd.concat([old_positions, new_positions], join= 'outer', axis=0, sort=True)
    new_positions.to_csv('nextBikeData.csv', index_label='date')

# TODO
# Use Database

# Connect to an existing database
# conn = psycopg2.connect("dbname=bikes user=postgres")
# Open a cursor to perform database operations
# cur = conn.cursor()

     # batch insert
# cur.execute(sql, (value1,value2))
# conn.commit()
# cur.close()
# conn.close()

except Exception as e:

    # TODO: notify if error occurs
    print (e.with_traceback())

