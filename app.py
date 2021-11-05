#Step1
from flask import Flask, jsonify

#Import numpy and datetime
import numpy as np
import datetime as dt
from datetime import timedelta
import re

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
        f"/api/v1.0/start/end"
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

    # Close the session
    session.close()

    return jsonify(precipitation_date_tobs)
    



#C Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_details = list(np.ravel(results))

    # Close the session
    session.close()

    return jsonify(station_details)



 #D tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the Database
    session = Session(engine)

    # Query Measurements for latest date and calculate query_start_date
    latest_date = (session.query(Measurement.date)
                          .order_by(Measurement.date
                          .desc())
                          .first())
    
    latest_date_str = str(latest_date)
    latest_date_str = re.sub("'|,", "",latest_date_str)
    latest_date_obj = dt.datetime.strptime(latest_date_str, '(%Y-%m-%d)')
    query_start_date = dt.date(latest_date_obj.year, latest_date_obj.month, latest_date_obj.day) - dt.timedelta(days=366)
     
    # Query station names and their observation counts sorted desc. and select most active station
    query_station_list = (session.query(Measurement.station, func.count(Measurement.station))
                             .group_by(Measurement.station)
                             .order_by(func.count(Measurement.station).desc())
                             .all())
    
    station = query_station_list[0][0]
    print(station)


    # Return a list of tobs for the year prior to the final date
    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs)
                      .filter(Measurement.date >= query_start_date)
                      .filter(Measurement.station == station)
                      .all())

    # Create JSON results
    tobs_list = []
    for result in results:
        line = {}
        line["Date"] = result[1]
        line["Station"] = result[0]
        line["Temperature"] = int(result[2])
        tobs_list.append(line)

    # Close the session
    session.close()

    return jsonify(tobs_list)


#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route('/api/v1.0/<start>')
def get_t_start(start):
    session = Session(engine)
    queryresult =  session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        
    session.close()



    tobs_list = []
    for date,min,avg,max in queryresult:
        line = {}
        line["Min"] = min
        line["Average"] = avg
        line["Max"] = max
        tobs_list.append(line)


  
    return jsonify(tobs_list)



#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route('/api/v1.0/<start>/<stop>')
def get_t_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobs_list = []
    for date,min,avg,max in queryresult:
        line = {}
        line["Min"] = min
        line["Average"] = avg
        line["Max"] = max
        tobs_list.append(line)

    return jsonify(tobs_list)

# Close the session
session.close()


# Step 3 Run code from command line
if __name__ == '__main__':
    app.run(debug=True)