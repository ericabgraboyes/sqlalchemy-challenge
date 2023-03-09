# import dependencies
import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, asc, desc
from sqlalchemy.sql import exists

from flask import Flask, jsonify
##################################################
# Database set up
##################################################

# save filepath to database
db = "../Resources/hawaii.sqlite"

# create engine
engine = create_engine(f"sqlite:///{db}")
# reflect an existing database into new model
Base = automap_base()

# reflect tables
Base.prepare(autoload_with=engine)

# save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

########################################################
# Define function to append values to dictionary key

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value

########################################################
# Flask set up
app = Flask(__name__)

########################################################
# Flask Routes
########################################################
@app.route("/")
def landing():
    """ List all available api routes."""

    return (
        f"Available Routes :<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"~~~ datesearch (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/datesearch/ <br/><br/><br/>"
        f"~~~ daterange  (enter as YYYY-MM-DD/YYYY-MM-DD)<br/>"
        f"/api/v1.0/daterange/"
    )

########################################################

# Flask Routes: Precipitation 
########################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """ return precipitation for last 12 months relativte to most recent date"""

    # query to find latest date
    last_dt = session.query(Measurement.date).distinct().\
        order_by(desc(Measurement.date)).first()
        
    last_dt = str(last_dt)
    last_dt = re.sub("'|,", "", last_dt)
    last_dt = dt.datetime.strptime(last_dt, '(%Y-%m-%d)')
    start_dt = dt.date(last_dt.year, last_dt.month, last_dt.day) - dt.timedelta(days=365)

    # query precipitation over last 12 months
    precipitation = session.query(Measurement.date, Measurement.prcp) .\
                filter(Measurement.date >= start_dt) .\
                filter(Measurement.prcp != 'null') .\
                order_by(desc(Measurement.date)).all()
    
    session.close()

    # create dictionary - key = date, value = prcp        
    dt_dict = {}

    for p in precipitation:
        append_value(dt_dict, p.date, p.prcp)

    return jsonify(dt_dict)

########################################################
# Flask Routes: Station list
########################################################
@app.route("/api/v1.0/stations")
def station():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station numbers / IDs """

    # run query, store results in variable
    stations = session.query(Measurement.station).distinct() .\
        order_by(asc(Measurement.station))
    
    session.close()
    
    # unpack query object into list
    station_list = []

    for s in stations:
        station_list.append(s.station)

    # create JSON result
    return jsonify(station_list)

########################################################
# Flask Routes: tobs 
########################################################
@app.route("/api/v1.0/tobs")
def most_activity():

    # create session object
    session = Session(engine)

    """Return last year of temperature for station USC00519281"""
    
    # (a) query station with most activity - use to filter date range
    most_station = (session.query(Measurement.station, func.count(Measurement.station))
                             .group_by(Measurement.station)
                             .order_by(func.count(Measurement.station).desc())
                             .first())
    
    station_filter = str(most_station[0])

    # (b) query latest date based on station with most activity"
    station_last_dt = session.query(Measurement.date).distinct().\
        filter(Measurement.station == station_filter).\
        order_by(desc(Measurement.date)).first()

    # find value of start_date, 1 year prior to station_last_dt    
    station_last_dt = str(station_last_dt)
    station_last_dt = re.sub("'|,", "", station_last_dt)
    station_last_dt = dt.datetime.strptime(station_last_dt, '(%Y-%m-%d)')
    station_start_dt = dt.date(station_last_dt.year, station_last_dt.month, station_last_dt.day) - dt.timedelta(days=365)

    # (c) query temperature filter on active station and date range 
    tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
            .filter(Measurement.date >= station_start_dt)\
            .filter(Measurement.station == station_filter)\
            .all()
    
    session.close()    

    # Create JSON Results
    tobs_list = []

    for t in tobs:
        tobs_list.append(t[1] + ": " + str(t[2])) 
 
    tobs_list.sort(reverse=True)
    
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)