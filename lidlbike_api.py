import requests 
import json
import pandas as pd
import datetime
import os
import time

# request data
# TODO: use two keys
#api key
key='Bearer xxx'
# api-endpoint 
URL = "https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals"
lat=52.520008
lon=13.404954
radius=10000 # radius in meter, max 10000 (10km)
providernetwork=2
expand='rentalObject'
limit = 50


offset = 0 # mit offset Blättern
more_bikes = True
new_positions = pd.DataFrame(index=[datetime.datetime.now()])

while more_bikes:
	try:
	
		#header
		# note in header
		headers = {"Authorization": key, "Accept": "application/json"}

		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'lat':lat, 'lon':lon, 'radius':radius, 'providernetwork':providernetwork, 'expand':expand, 'limit':limit, 'offset':offset} 

		# sending get request and saving the response as response object 
		response = requests.get(url = URL, params = PARAMS, headers=headers) 

		#Todo error handling
		r = response.json()

		# format output csv
		for i in range(len(r['items'])):
			new_positions[r['items'][i]['rentalObject']['providerRentalObjectId']] = str(r['items'][i]['position']['coordinates'])

		# get all paginations
		offset += 50
		items = len(r['items'])
		if len(r['items']) < 50:
			more_bikes = False

		# 30 calls max per minute (then timeout)
		if (offset % 1500 == 0):
			# TODO: loop two keys
			time.sleep(90)

	except Exception as e:
		# TODO: send email if error occurs
		print (e.with_traceback())

# write new positions in csv file
if os.path.isfile('./lidlBikeData.csv'):
	old_positions = pd.read_csv('lidlBikeData.csv', index_col=0)
	new_positions = pd.concat([old_positions, new_positions], join= 'outer', axis=0, sort=True)

new_positions.to_csv('lidlBikeData.csv', index_label='date')
		
		
		# TODO: test for returned error
		# TODO: test for changed order in new data
		# TODO: test for new bike added
		# TODO: test for old bike removed
		# TODO: test for bike reentering


