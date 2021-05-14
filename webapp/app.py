# This is a very basic Flask application for exploring transit data on a map
# Note: In order to run this app, make sure to export FLASK_APP=webapp/app.py from the root dir
# Note: For auto-reload and dev environment, also use export FLASK_ENV=development

# TODO: Seperate views out into a new file exclusively for routes
# TODO: Configuration and setup need to be 

from flask import Flask, render_template, jsonify
from . import db

# Create application instance
app = Flask(__name__)

@app.route('/')
def home_page():
    agencies = db.list_agencies()
    return render_template('home.html', agencies=agencies, title="Home")

@app.route('/errors/<agency>/<route>')
def errors_page(agency, route):
    agency = agency
    route = route
    return render_template('errors.html', agency=agency, route=route, title="Errors")

@app.route('/about')
def about_page():
    return render_template('about.html', title="About the app")

@app.route('/map/<agency>')
def map_page(agency):
    agencies = db.list_agencies()
    agency_data = None
    for a in agencies:
        if a['agency_name'] == agency:
            agency_data = a
            break
    routes = db.list_routes(agency)
    current_route = None
    return render_template('map.html', agency_data=agency_data, agency=agency, routes=routes, current_route=current_route, title=agency)

# Pseudo-API URL's to return data for the app
# TODO: Seperate these out into a proper API
@app.route('/route/<agency>/<route_id>')
def get_route_shape(agency, route_id):
    # Turn raw data into a JSON obect consisting of all shapes and directions
    shapes = db.get_route_shape(agency, route_id)
    data = {'shapes': [], 'data': {}}

    # Note this is not the correct format for GeoJSON type data structures
    # TODO: Format it to GeoJSON spec into feature collections, etc.
    for s in shapes:
        if s[0] not in data['shapes']:
            data['shapes'].append(s[0])
            data['data'][s[0]] = {'route': int(s[1]), 'direction': int(s[2]), 'path': [[float(s[4]), float(s[3])]]}
        else:
            data['data'][s[0]]['path'].append([float(s[4]), float(s[3])])
            
    return jsonify(data)

@app.route('/trips/<agency>/<route_id>')
def get_recorded_trips(agency, route_id):
    # Get all real-time positions recorded for this route
    trips = db.get_trips_for_routes(agency, route_id)
    return jsonify(trips)

@app.route('/agency_info/<agency>')
def get_agency_info(agency):
    agencies = db.list_agencies()
    agency_data = None
    for a in agencies:
        if a['agency_name'] == agency:
            agency_data = a
            break
    return jsonify(agency_data)

# Run in debug mode if the this file is launched directly
if __name__ == '__main__':
   app.run(debug = True)