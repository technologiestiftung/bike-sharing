import pandas as pd
import numpy as np
import json
import psycopg2
from psycopg2.extras import RealDictCursor

dbhost = 'localhost'
dbname = 'backup-bikes'
dbuser = 'postgres'
dbpassword = 'Spuck8/Crews'

def preprocess(df):
    
    MODE_TRIP = 'trip'
    MODE_ACCESS = 'accessible'

    df['end_timestamp'] = None
    df['next_lat'] = None
    df['next_lon'] = None
    df['mode'] = None

    df.sort_values(by=['bikeId', 'timestamp'], inplace = True)
    df['end_timestamp'] = df.timestamp.shift(-1)

    # set location of next occurence
    df['next_lat'] = np.where(df.bikeId == df.bikeId.shift(-1), df.latitude.shift(-1), None)
    df['next_lon'] = np.where(df.bikeId == df.bikeId.shift(-1), df.longitude.shift(-1), None)
    
    # if the bike has moved its a trip, otherwise the bike was accessible at its location
    df['mode'] = np.where((df.latitude != df.next_lat) | (df.longitude != df.next_lon), MODE_TRIP, MODE_ACCESS)
    
    # if bike Id is not the same as next, then this is the final time stamp and the next_timestamp is set to None
    df['end_timestamp'] = df.end_timestamp.where(df.bikeId == df.bikeId.shift(-1),None, axis=0)
    
    # delete last instances of all bikes
    df = df[df.next_lat.notnull()]
    return df

sql = """
SELECT id, "bikeId", "providerId", "timestamp", latitude, longitude
	FROM public."bikeLocations"
	WHERE ("timestamp" >  current_date - INTERVAL '1 day') and ("timestamp" < current_date);
"""
    
conn = psycopg2.connect("host=" + dbhost + " dbname=" + dbname + " user=" + dbuser + " password=" + dbpassword)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute(sql)

date = '2019-x-x'
df = pd.DataFrame(cur.fetchall())
df = preprocess(df)
df.to_json('../../../html/bike-data/data-' + date + '.json', orient='records')
# 