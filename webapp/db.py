# DB handler for the app
# TODO: Models need to be seperated out from DB function, right now it's all mashed together, super ugly

# Helper class with useful application specific functions
import DBTools.PostgresDBHelper as PGDBH

from flask import current_app, g
from flask.cli import with_appcontext

# This returns a database connection for the applciation to use, note: Postgres seems to require seperate 
#   connections for connecting to different databases so likely this method will run into strange errors
# TODO: Turn this into a context manager, because it seems the application never closes the connection 

def get_db():
    if 'db' not in g:
        g.db = PGDBH.PostgresDBHelper(host="localhost", user="postgres", password="1234", database="postgres")
        g.db.connect()
    return g.db

# Generally, a db connection should only be created once and reused until final closing, but Postgres requires
#   new connections, the psycopg2 backend requires new connections to switch databases
def close_db(e=None):
    db = g.pop('db', None) # get rid of our db variable off of the app context variable
    if db is not None:
        db.disconnect()

# Get list of agencies we have in the database, currently additional data is appended ad-hoc
# TODO: Seperate out model, ideally reusing the model orginally created to store the data
def list_agencies():
    dbc = get_db()
    agencies = dbc.get_agencies(active=False)

    # add on some additional information for each of our agencies
    for agency in agencies:
        # this part is super hacky, but for now we just need basic lat/lng for a few agencies
        if agency['agency_name'] == 'victoria':
            agency['lat'] = -123.4
            agency['lng'] = 48.4
            count = dbc.get_realtime_vehicle_positions_count(agency['agency_name'])
            agency['count'] = count
        elif agency['agency_name'] == 'adelaide':
            agency['lat'] = 138.6
            agency['lng'] = -34.9
            count = dbc.get_realtime_vehicle_positions_count(agency['agency_name'])
            agency['count'] = count
        else:
            agency['lat'] = None
            agency['lng'] = None
            agency['count'] = 'no data'
    return agencies

def list_routes(agency_name):
    dbc = get_db()
    routes = dbc.get_routes(agency_name)
    return routes

def get_route_shape(agency_name, route_id):
    dbc = get_db()
    shapes = dbc.get_route_shape(agency_name, route_id)
    return shapes

def get_trips_for_routes(agency_name, route_id):
    dbc = get_db()
    trips = dbc.get_trips(agency_name, route_id)
    data = {'data' : {}, 'trips': [], 'metadata': {} }
    for row in trips:
        trip_id = row[2]
        lat = row[14]
        lng = row[15]
        # we only want valid data
        if trip_id is not None and lat is not None and lng is not None:
            # create new blank entry for this trip_id
            if trip_id not in data['trips']:
                data['trips'].append(trip_id)
                data['data'][trip_id] = []
                data['metadata'][trip_id] = row
            data['data'][trip_id].append([float(lng),float(lat)])
    return data

# TODO: get all recorded vehicle positions for this route
def get_trips(route):
    pass
