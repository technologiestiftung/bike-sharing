import math
from itertools import permutations, repeat
import numpy as np

# 500 m radius is covered by mobike request
radius = 500

# number of km per degree = ~111km 
# (between 110.567km at the equator and 111.699km at the poles)
# 1km in degree = 1 / 111.32km = 0.0089
# 1m in degree = 0.0089 / 1000 = 0.0000089
coef = 2*radius * 0.0000089

# bounding box Berlin
# start_lat = 52.341823
# start_long = 13.088209
# end_lat = 52.669724
# end_long = 13.760610

# small bounding box Berlin
end_lat = 52.536654
end_long = 13.449012
start_lat = 52.482990
start_long = 13.306624

def get_new_lat(old_lat):
    return (old_lat + coef)

# pi / 180 = 0.018
def get_new_long(old_long):
    return (old_long + coef / math.cos(start_lat * 0.018))

# get all lats:
first_row_lats = []
second_row_lats = []
current_lat1 = start_lat
current_lat2 = start_lat + radius * 0.0000089
while current_lat1 < end_lat:
    first_row_lats.append(current_lat1)
    second_row_lats.append(current_lat2)
    current_lat1 = get_new_lat(current_lat1)
    current_lat2 = get_new_lat(current_lat2)

# get all longs:
first_row_longs = []
second_row_longs = []
current_long1 = start_long
current_long2 = start_long + (radius * 0.0000089) / math.cos(start_lat * 0.018)
while current_long1 < end_long:
    first_row_longs.append(current_long1)
    second_row_longs.append(current_long2)
    current_long1 = get_new_long(current_long1)
    current_long2 = get_new_long(current_long2)

all_coordinates = np.array([]).reshape(0,2)
for long in first_row_longs:
    coordinates = np.array(list(zip(first_row_lats, np.repeat(long, len(first_row_lats)))))
    all_coordinates = np.append(all_coordinates, coordinates, axis = 0)

for long in second_row_longs:
    coordinates = np.array(list(zip(second_row_lats, np.repeat(long, len(second_row_lats)))))
    all_coordinates = np.append(all_coordinates, coordinates, axis = 0)

#np.savetxt("coordinates.csv", all_coordinates, header= 'lat, long', delimiter=",", fmt="%10.6f")
np.savetxt('coordinates.txt', all_coordinates, delimiter=", ", header="[", newline = "],[", footer = "]", fmt="%10.6f")