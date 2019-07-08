import pandas as pd
import numpy as np
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
import config

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

def cleaning(df):
    # switch lat lon where it's wrong (for Berlin)
    temp = df['latitude']
    df.loc[(df.latitude < 15),'latitude'] = df.loc[(df.latitude < 15),'longitude']
    df.loc[(df.latitude < 15),'longitude'] = temp

    # delete instances with unplausible locations
    df.drop(df[df.longitude > 13.7].index, inplace=True)
    df.drop(df[df.next_lon > 13.7].index, inplace=True)

    df.drop(df[df.longitude < 13.0].index, inplace=True)
    df.drop(df[df.next_lon < 13.0].index, inplace=True)

    df.drop(df[df.latitude > 52.7].index, inplace=True)
    df.drop(df[df.next_lat > 52.7].index, inplace=True)

    df.drop(df[df.latitude < 52.3].index, inplace=True)
    df.drop(df[df.next_lat < 52.3].index, inplace=True)

    df['duration'] = df.end_timestamp - df.timestamp

    # drop bikeId for pseudonymisation
    df.drop('bikeId', axis=1, inplace=True)
    return df


conn = psycopg2.connect("host=" + config.dbhost + " dbname=" + config.dbname + " user=" + config.dbuser + " password=" + config.dbpassword)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute(sql)

date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
df = pd.DataFrame(cur.fetchall())
df = preprocess(df)
df = cleaning(df)
df.to_json('../../../html/bike-data/' + date + '-data.json', orient='records')
# 