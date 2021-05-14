# Google Transit Feed Specification (GTFS) sample application using real-time scripts
This repository contains helper scripts to download real-time data from agencies using the GTFS, and build temporal datasets for reserach and analysis. This enables paths/trajectories of vehicles to be generated for geospatial applications.

Also included is a sample app built in Flask to showcase what this data looks like and overlay multiple recorded trajectories for a given route. Using the app, route ground truths can be explored as well.

Before attempting to run the application, it is highly recommended a virtual environment be used. For example, it can be created with:

```
virtualenv appenv
```

Note: This example is on Mac and assumes virutalenv has been installed via Homebrew.

To use the application, a running PostgreSQL instance is necessary. If starting from scratch, the SQL scripts in the DBScripts folder can be used to generate empty schemas for data load. The following resources need to be updated or added:

1. GTFS-FEEDS.csv contains basic information about a particular feed, i.e. the url at which its static/real-time data can be downloaded from, update frequency, etc.
2. Static data for a given agency can be added manually under the static_zips folder/[AGENCY NAME]/static
3. A running PostgreSQL instance with a user that has general elevated privileges such as create, drop, update, etc.

Next, the database scripts can be run in the following order: first use create_agencies_table.sql to create the general information about agencies from the above mentioned csv file, and then use the create_sample_tables.sql script to create a sample set of databases and tables to store static data. This sample is used whenever a new agency is added, and its corresponding information needs to be created.

At this point, enough information has been provided to the application to visualize tracks, but no real-time trajectories are available. The runner.py script can be used for this purpose. This script will load real-time information at fixed intervals for every agency we have defined in our database. This information will be parsed and loaded to the respective agency's database only when an update to the feed is recognized. Note, currently the script only loads vehicle positions, but other real-time feeds are available as well, such as alerts.

Once the runner.py script has been run for a desired period of time, real-time data is now loaded into the database for each agency.

To view the application the path to the Flask application must be provided to the running environment (terminal for example):

```
export FLASK_APP=webapp/app.py
```

Optionally, a development flag can also be added but this application is currently only built in a development mode so it should force to run in this mode:

```
export FLASK_ENV=development
```

Finally, to run the app simply type the following:

```
flask run
```

A message should be display showing where to view the app, for example:

```
* Serving Flask app "webapp/app.py" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* ...
```

Navigating to the the url described, the application should be visible.
