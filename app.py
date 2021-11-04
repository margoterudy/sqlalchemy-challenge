#Step1
from flask import Flask, jsonify

#Import numpy and datetime
import numpy as np
import datetime as dt

# Import Dependencies Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#############################
# Database Setup
#############################
engine  = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


#Tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#############################
# Flask Setup
#############################
#step2
app = Flask(__name__)

#Step 4 python function home index route (is the page running, is it showing my info? YES!)
#A Home
@app.route("/")
def Home():
    "List of API routes."
    return(
        f"List of API routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"

    )

#B Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():


    # Query Measurement
    results = (session.query(Measurement.date, Measurement.tobs)
                      .order_by(Measurement.date))
    
    # Create a dictionary
    precipitation_date_tobs = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        precipitation_date_tobs.append(dt_dict)

    return jsonify(precipitation_date_tobs)
    
# Close the session
session.close()

   



#C Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_details = list(np.ravel(results))

    return jsonify(station_details)


# Close the session
session.close()



# #D tobs
# @app.route("/api/v1.0/tobs")
# def tobs():


#E Return a JSON lists


# Step 3 Run code from command line
if __name__ == '__main__':
    app.run(debug=True)