from app import Artist, Show, Venue

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/fyyur'
db = SQLAlchemy(app)


with app.app_context():
  show1 = Show(venue_id=1, artist_id=1, start_time="2019-05-21T21:30:00.000Z")
  show2 = Show(venue_id=3, artist_id=2, start_time="2019-06-15T23:00:00.000Z")
  show3 = Show(venue_id=3, artist_id=3, start_time="2035-04-01T20:00:00.000Z")
  show4 = Show(venue_id=3, artist_id=3, start_time="2035-04-08T20:00:00.000Z")
  show5 = Show(venue_id=3, artist_id=3, start_time="2035-04-15T20:00:00.000Z")
  db.session.add(show1)
  db.session.add(show2)
  db.session.add(show3)
  db.session.add(show4)
  db.session.add(show5)
  db.session.commit()