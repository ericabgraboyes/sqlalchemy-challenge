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
    # last_dt = session.query(Measurement.date).distinct().\
    #     order_by(desc(Measurement.date)).first()
        
    # last_dt = str(last_dt)
    # last_dt = re.sub("'|,", "", last_dt)
    # last_dt = dt.datetime.strptime(last_dt, '(%Y-%m-%d)')
    # start_dt = dt.date(last_dt.year, last_dt.month, last_dt.day) - dt.timedelta(days=365)

    # query precipitation over last 12 months
    precipitation = session.query(Measurement.date, Measurement.prcp) .\
                filter(Measurement.date >= ('2016-08-23')) .\
                filter(Measurement.prcp != 'null') .\
                order_by(desc(Measurement.date)).all()
    
    session.close()

    # create dictionary - key = date, value = prcp        
    dt_dict = {}

    for p in precipitation:
        append_value(dt_dict, p.date, p.prcp)

    return jsonify(dt_dict)

if __name__ == '__main__':
    app.run(debug=True)