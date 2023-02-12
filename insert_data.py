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

venue1 = Venue(id=1, name="The Musical Hop", city="San Francisco", 
  state="CA", address="1015 Folsom Street", phone="123-123-1234", 
  image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60", 
  facebook_link="https://www.facebook.com/TheMusicalHop", 
  website="https://www.themusicalhop.com", 
  seeking_talent=True, seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
  genres="Jazz,Reggae,Swing,Classical,Folk")
venue2 = Venue(id=2, name="The Dueling Pianos Bar", city="New York", 
  state="NY", address="335 Delancey Street", phone="914-003-1132", 
  image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80", 
  facebook_link="https://www.facebook.com/theduelingpianos",
  website="https://www.theduelingpianos.com", 
  seeking_talent=False, seeking_description="",
  genres="Classical,R&B,Hip-Hop")
venue3 = Venue(id=3, name="Park Square Live Music & Coffee", city="San Francisco", 
  state="CA", address="34 Whiskey Moore Ave", phone="415-000-1234", 
  image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80", 
  facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  website="https://www.parksquarelivemusicandcoffee.com", 
  seeking_talent=False, seeking_description="",
  genres="Rock n Roll,Jazz,Classical,Folk")

# artist1 = Artist(name=, city=, state=, phone=, genres=, image_link=, facebook_link=)


artist4 = Artist(id=4, name="Guns N Petals", city="San Francisco", state="CA", phone="326-123-5000", genres="Rock n Roll", 
  image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80", 
  facebook_link="https://www.facebook.com/GunsNPetals", 
  website="https://www.gunsnpetalsband.com", seeking_venue = True, 
  seeking_description="Looking for shows to perform at in the San Francisco Bay Area!")
artist5 = Artist(id=5, name="Matt Quevedo", city="New York", state="NY", phone="300-400-5000", genres="Jazz",
  image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80", 
  facebook_link="https://www.facebook.com/mattquevedo923251523", 
  website="", seeking_venue = False, 
  seeking_description="")
artist6 = Artist(id=6, name="The Wild Sax Band", city="San Francisco", state="CA", phone="432-325-5432", genres="Jazz,Classical", 
  image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80", 
  facebook_link="", 
  website="", seeking_venue = False, 
  seeking_description="")





with app.app_context():
  db.session.add(venue1)
  db.session.add(venue2)
  db.session.add(venue3)
  db.session.add(artist4)
  db.session.add(artist5)
  db.session.add(artist6)
  db.session.commit()
  show1 = Show(venue_id=1, artist_id=4, start_time="2019-05-21T21:30:00.000Z")
  show2 = Show(venue_id=3, artist_id=5, start_time="2019-06-15T23:00:00.000Z")
  show3 = Show(venue_id=3, artist_id=6, start_time="2035-04-01T20:00:00.000Z")
  show4 = Show(venue_id=3, artist_id=6, start_time="2035-04-08T20:00:00.000Z")
  show5 = Show(venue_id=3, artist_id=6, start_time="2035-04-15T20:00:00.000Z")
  db.session.add(show1)
  db.session.add(show2)
  db.session.add(show3)
  db.session.add(show4)
  db.session.add(show5)
  db.session.commit()

 
'''
Venue===
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,

"id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  
   "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,

Artist====


data1={
    "id": 4,
    "name": "Guns N Petals",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
 data2={
    "id": 5,
    "name": "Matt Quevedo",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }

 data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
    
'''