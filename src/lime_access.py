import requests 
import json
import pandas as pd
import datetime
import os
import psycopg2
import psycopg2.extras
import traceback
import config
import time
import logging



def get_login_code():
    headers = {"Accept": "application/json"}
    
    PARAMS = {"phone": config.phone_no}

    # sends a login_code to the phone number
    requests.get(url = URL, params = PARAMS, headers=headers) 

def get_session_token():
    headers = {"Accept": "application/json"}

    #login code from text message
    PARAMS = {"login_code": config.login_code, "phone": config.phone_no}

    # sends a login_code to the phone number
    response = requests.post(url = URL, params = PARAMS, headers=headers) 
    # r = response.json()
    print (response.json())

    session = requests.Session()
    print ("------------------------")
    print (session.cookies.get_dict())

def get_data(token):
    URL = "https://web-production.lime.bike/api/rider/v1/views/map"
    key = "Bearer " + token
    HEADERS = {"Authorization": key, "Accept": "application/json"}
    session = requests.Session()
    response = session.get(URL)
    cookie = session.cookies.get_dict()["_limebike-web_session"]
    COOKIES = {"_limebike-web_session": cookie}

    PARAMS = {"ne_lat": ne_lat, "ne_lng": ne_lng, "sw_lat": sw_lat, "sw_lng": sw_lng, "user_latitude": user_lat, "user_longitude": user_lng,  "zoom": 12}

    # sending get request and saving the response as response object 
    response = requests.get(url = URL, params = PARAMS, headers=HEADERS, cookies = COOKIES) 
    r = response.json()
    limebikes = []
    print (len(r['data']['attributes']['bikes']))
    for i in range(len(r['data']['attributes']['bikes'])):
        bike_id = r['data']['attributes']['bikes'][i]['id']
        bike_lat = r['data']['attributes']['bikes'][i]['attributes']['latitude']
        bike_lon = r['data']['attributes']['bikes'][i]['attributes']['longitude']
        limebikes.append([bike_lat, bike_lon])

    pd.DataFrame(limebikes).to_csv('limebikes_output.csv', index=False)
                    
if __name__== "__main__":
    URL = "https://web-production.lime.bike/api/rider/v1/login"

    #Berlin lat lon
    # radius_center_lat=52.520008
    # radius_center_lon=13.404954
    user_lat=52.520000
    user_lng=13.404954

    sw_lat = 52.461561
    sw_lng = 13.302729
    ne_lat = 52.556812
    ne_lng = 13.373722
    
    # 1. get login code
    # get_login_code()

    # 2. get token with login code
    # get_session_token(login_code)

    # 3. get data
    token = config.lime_token
    get_data(token)
    