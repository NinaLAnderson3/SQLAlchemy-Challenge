#1. Import Flask
from flask import Flask, jsonify
import numpy as np
#
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# #
# # # ##########Database setup################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# # #
# # # # reflect an existing database into a new model
Base = automap_base()
# # # reflect the tables
# Base.prepare(engine, reflect=True)

# # ##Save references to tables###
Measurements = Base.classes.Measurement
Stations = Base.classes.station
# ##Flask setup
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
    )


if __name__ == '__main__':
    app.run(debug=True)
