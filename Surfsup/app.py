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