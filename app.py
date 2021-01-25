#1. Import Flask
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# ##########Database setup################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#
# # reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)

# ##Save references to tables###
Measurements = Base.classes.Measurement
Stations = Base.classes.station
##Flask setup
app = Flask(__name__)

#3. Define what to do when user hits the home page
@app.route("/")
def home():
    print("Server received request for Home Page.")
    return (
    f"Welcome to the climate analysis page!<br/>"
    f"Available routes:<br/>"
    f'/api/v1.0/precipitation<br/>'
    f'/api/v1.0/stations<br/>'
    f'/api/v1.0/tobs<br/>'
    f'/api/v1.0/prior_year_tobs<br/>'
    f'/api/v1.0/agg_temps<br/>'
    )


# @app.route('api/v1.0/precipitation')
def precipation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurment.prcp).all()
    session.close()
#
#     # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp_data = []
    for date, prcp in results:
        all_dict = {}
        date_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp_data.append(all_dict)
#
        return jsonify(all_prcp_data)
#
@app.route('/api/v1.0/stations')
def stations():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of all station names"""
        # Query all passengers
        results = session.query(Stations.name).all()

        session.close()
#
#         # Convert list of tuples into normal list
        stations = list(np.ravel(results))

        return jsonify(stations)
# ####Temperature database#####
#
@app.route('api/v1.0/tobs')
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurment.tobs).all()
    session.close()
#
#     # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs_data = []
    for date, tobs in results:
        dict = {}
        date_dict["date"] = date
        prcp_dict["tobs"] = tobs

        all_tobs_data.append(dict)

        return jsonify(all_tobs_data)
#
#
if __name__ == '__main__':
    app.run(debug=True)
