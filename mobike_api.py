import requests 
import json
import pandas as pd
import datetime
import os
import time

# request data
URL = "http://app.mobike.com/api/nearby/v4/nearbyBikeInfo"
lat=52.520008
lon=13.404954
plattform= '1'
new_positions = pd.DataFrame(index=[datetime.datetime.now()])

# header
headers = {"plattform": plattform, \
    "Content-Type": "application/x-www-form-urlencoded", \
    "User-Agent" : "Mozilla/5.0 (Android 7.1.2; Pixel Build/NHG47Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.9 NTENTBrowser/3.7.0.496 (IWireless-US) Mobile Safari/537.36"}

# TODO: list of all radius centers
lat2=52.491503
lon2=13.345210
radius_centers = pd.read_csv("coordinates.csv")
new_positions = pd.DataFrame(index=[datetime.datetime.now()])

for i in range (radius_centers.shape[0]):
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'latitude': radius_centers.iloc[i, 0], 'longitude': radius_centers.iloc[i, 1]}

    # sending get request and saving the response as response object 
    response = requests.get(url = URL, params = PARAMS, headers = headers) 

    #Todo error handling
    r = response.json()

    if r['code'] == 0:
        for i in range(len(r['bike'])):
            new_positions[r['bike'][i]['distId'][1:]] = str(r['bike'][i]['distY']) + ', ' + str(r['bike'][i]['distX'])
    
    else:
        # TODO: errorhandling
        print('error: ' + r['message'])

# write new positions in csv file
if os.path.isfile('./mobikeData.csv'):
	old_positions = pd.read_csv('mobikeData.csv', index_col=0)
	new_positions = pd.concat([old_positions, new_positions], join= 'outer', axis=0, sort=True)

new_positions.to_csv('mobikeData.csv', index_label='date')

