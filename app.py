import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
        order_by(Measurement.date).all()

    year_rain = dict(precip_query)

    return jsonify(year_rain)

@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Station.id, Station.station).all()

    station_dict= dict(station_query)

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    temp_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
        order_by(Measurement.date).all()

    tobs_dict = dict(temp_query)

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    for x in query:
        result = list(x)

    start_list = dict(zip(['Min', 'Avg', 'Max'], result))

    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def trip(start_date, end_date):
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    for x in query:
        result = list(x)

    trip_list = dict(zip(['Min', 'Avg', 'Max'], result))

    return jsonify(trip_list)

if __name__ == '__main__':
    app.run(debug=True)
