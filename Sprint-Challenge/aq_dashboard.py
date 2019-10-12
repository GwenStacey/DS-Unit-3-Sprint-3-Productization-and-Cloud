"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\charl\\Documents\\MyGithub\\DS-Unit-3-Sprint-3-Productization-and-Cloud\\Sprint-Challenge\\db.sqlite3'
API = openaq.OpenAQ()
DB = SQLAlchemy()

DB.init_app(APP)

@APP.route('/', methods=['GET'])
def root():
    """Base view."""
    
    records = Record.query.filter(Record.value >= 10).all()
    return str(records)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    #def __repr__(self):
    #    return 'TODO - write a nice representation of Records'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    add_data()
    DB.session.commit()
    return 'Data refreshed!'

def get_data(val_list):
    msrmnt = API.measurements(city='Los Angeles', parameter='pm25')
    body = msrmnt[1]
    results = body['results']
    for i in results:
        val_list.append((i['date']['utc'], i['value']))
    return val_list

def add_data():
    utc_val = []
    get_data(utc_val)
    k = 0
    for i in utc_val:
        utc = i[0]
        val = i[1]
        val_utc = Record(id=k, datetime=str(utc), value=val)
        k += 1
        DB.session.add(val_utc)
    DB.session.commit()
