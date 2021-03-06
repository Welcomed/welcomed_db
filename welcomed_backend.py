# -*- coding: utf-8 -*-
"""
    welcomed_backend
    Backend server and database for the Welcomed app
    Requires key.py which contains GOOG_KEY, a string containing
    a google maps API key.
    For instructions on running this, see repo
    https://github.com/Welcomed/welcomed_db
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, Response, request, session, g, redirect, url_for, abort, \
     render_template, flash
import urllib, json, time
from flask.ext.cors import CORS, cross_origin
from key import GOOG_KEY


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'welcomed.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('loaddata')
def load_data():
    get_data('hospital', 'hospital', 'hospitals')
    get_data('general practice', 'doctor', 'doctors')
    get_data('psychologist', 'doctor', 'mentalhealth')
    get_data('real estate', 'real_estate_agency', 'realestate')

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_data(keyword, placetype, table):
    url1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+GOOG_KEY+"&location=-37.825358,144.995339&radius=10000&type="+placetype+"&keyword="+keyword
    url2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+GOOG_KEY+"&pagetoken="

    next_page_token = ""

    for url in [url1, url2]:
        if url == url2 and next_page_token:
            url += next_page_token
        time.sleep(10)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for place in data['results']:
            name = place['name']
            print name
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            address = place['vicinity']
            db = get_db()
            db.execute('insert into '+ table + ' (name, latitude, longitude, address) values (?, ?, ?, ?)',
                       [name, lat, lng, address])
            db.commit()
        if 'next_page_token' in data:
            next_page_token = data['next_page_token']

@app.route('/data/<table>')
@cross_origin()
def show_entries(table):
    db = get_db()
    cur = db.execute('select name, latitude, longitude, address from '+table+' order by id desc')
    entries = cur.fetchall()
    lst = [{'name':entry['name'], 'lat':entry['latitude'], 'lng':entry['longitude'], 'address':entry['address']} for entry in entries]
    resp = Response(response=json.dumps(lst), status=200, mimetype="application/json")
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
