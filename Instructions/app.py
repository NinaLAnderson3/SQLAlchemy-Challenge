#1. Import Flask
from flask import Flask, jsonify
import numpy as np
import datetime as dt

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
Measurement = Base.classes.measurement
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
    f'/api/v1.0/start_date<br/>'
    f'/api/v1.0/start_to_end_date<br/>'
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
#
#     # Create a dictionary from the row data and append to a list of all_passengers
    prcp_data = {date:prcp for date, prcp in results}

    # for date, prcp in results:
    #     # all_dict = {}
    #     date["date"] = date
    #     date["prcp"] = prcp

        # all_prcp_data.append(date)
#
    return jsonify(prcp_data)
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
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    year_range = dt.date(2011,1,1) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_range).\
    filter(Measurement.station == "USC00519281").all()

    session.close()
#
#     # Create a list from the row data
    temp = list(np.ravel(results))
    return jsonify(temp)
#

@app.route('/api/v1.0/start_date')
def start_date():
    session = Session(engine)
    start_date = dt.date(2010,1,1)
    tobsresults = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    aggs = list(np.ravel(tobsresults))

    return f'The highest temperature since {start_date} was {aggs[0]}.The average temperature since {start_date} is {aggs[2]}. The lowest temperature since {start_date} was {aggs[1]}'

    session.close()
#
@app.route('/api/v1.0/start_to_end_date')
def start_to_date():
    session = Session(engine)
    start_date = dt.date(2010,1,1)
    end_date = dt.date(2010,12,31)
    range_data = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date < end_date).all()

    aggs2 = list(np.ravel(range_data))

    return f'The highest temperature between {start_date} and {end_date} was {aggs2[0]}.The average temperature between {start_date} and {end_date} was {aggs2[2]}. The lowest temperature between {start_date} and {end_date} was {aggs2[1]}'

    session.close()
#
if __name__ == '__main__':
    app.run(debug=True)
