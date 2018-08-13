import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation levels in the last year"""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date 1 year ago from today
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    prcp = session.query(Measurement.date,Measurement.prcp).\
        order_by(Measurement.date).all()

# Create a dictionary from returned list
    results = dict(prcp)
    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Query all passengers
    station_results = session.query(Station.id, Station.station).all()

    station_dict = dict(station_results)

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all precipitation levels in the last year"""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(last_date)

# Calculate the date 1 year ago from today
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    print(one_year_ago)

# Perform a query to retrieve the data and precipitation scores
    tobs_results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date > one_year_ago).\
        order_by(Measurement.date).all()

# Create a dictionary from returned list
    tobs_results_dict = dict(tobs_results)
    return jsonify(tobs_results_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Fetch a JSON list of minimum temperatures, average temperatures, and max temperatures for a given start"""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Fetch a JSON list of minimum temperatures, average temperatures, and max temperatures for a given start"""
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)
