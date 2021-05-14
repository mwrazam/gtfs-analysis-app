# pylint: disable=E1101
import json
import time
import urllib.request
from datetime import datetime

from google.protobuf.json_format import MessageToJson
from google.transit import gtfs_realtime_pb2

import DBTools.PostgresDBHelper as PGDBH


def download_vehicle_positions(url):
    # use the url to get the data and download and parse it
    data = {'cols': ['timestamp', 'trip', 'vehicle', 'lat', 'lng', 'bearing', 'speed', 'vehicle_timestamp', 'congestion', 'occupancy'], 'data': []}

    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = urllib.request.urlopen(url)
        feed.ParseFromString(response.read())
        ts = feed.header.timestamp
        for e in feed.entity:
            row = [ts, e.vehicle.trip.trip_id, e.vehicle.vehicle.id, e.vehicle.position.latitude, e.vehicle.position.longitude, e.vehicle.position.bearing, e.vehicle.position.speed, e.vehicle.timestamp, '', '']
            data['data'].append(row)
    except Exception as inst:
        print(inst)
        print("Failed :(")

    finally:
        pass

    return ts, data

def run():
    dbc = PGDBH.PostgresDBHelper(host="localhost", user="postgres", password="1234", database="postgres")
    dbc.connect()

    print(f"{'*'*100}")


    agencies = dbc.get_agencies(active=True)
    while True: # right now our download loop runs forever
        for agency in agencies:
            if 'timestamp' not in agency.keys():
                agency['timestamp'] = ""
            if 'counter' not in agency.keys():
                agency['counter'] = 0
            data_timestamp, new_data = download_vehicle_positions(agency['vehicle_positions'])
            #print(f"current timestamp:{agency['timestamp']}, data timestamp: {data_timestamp}")
            if data_timestamp != agency['timestamp']:
                agency['counter'] = agency['counter'] + 1
                agency['timestamp'] = data_timestamp
                print(f"{agency['agency_name']} {data_timestamp} Run #:{agency['counter']} [{len(new_data['data'])} rows]")
                dbc.insert_position_update(agency['agency_name'], new_data)
        time.sleep(5)
    dbc.disconnect()
            
if __name__ == '__main__':
    run()
