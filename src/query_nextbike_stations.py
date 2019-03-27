import requests 
import datetime
import psycopg2
import traceback
import config 

if __name__== "__main__":

    query_date= datetime.datetime.now()

    # request data
    URL = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_bn/en/station_information.json"

    # sending get request and saving the response as response object 
    response = requests.get(url = URL) 
    try:
        r = response.json()
        conn = psycopg2.connect("host=" + config.dbhost + " dbname=" + config.dbname + " user=" + config.dbuser + " password=" + config.dbpassword)
        cur = conn.cursor()
        nextbikes = []
        
        for i in range(len(r['data']['stations'])):
            station_id = int(r['data']['stations'][i]['station_id'])
            
            name = r['data']['stations'][i]['name']
            short_name = r['data']['stations'][i]['short_name']
            if "capacity" in r['data']['stations'][i]: 
                capacity = r['data']['stations'][i]['capacity']
            else:
                capacity = None
            lat = r['data']['stations'][i]['lat']
            lon = r['data']['stations'][i]['lon']

            # insert into db - update "last listed" of existing stations with every new query and add new stations
            cur.execute("""
                INSERT INTO public."stations" ("id", "latitude", "longitude", "firstListed", "lastListed", "name", "short_name", "capacity")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT ("id") DO UPDATE SET "lastListed" = %s;
                """,
                (station_id, lat, lon, query_date, query_date, name, short_name, capacity, query_date))
            
        conn.commit()
        cur.close()
        conn.close()

    except Exception:
        traceback.print_exc()
