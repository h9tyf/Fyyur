#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    @hybrid_property
    def past_shows(self):
      currentDateTime = datetime.now()
      res = db.session.query(Show).filter_by(venue_id=self.id).filter(Show.start_time < currentDateTime).all()
      return res
    @hybrid_property
    def upcoming_shows(self):
      currentDateTime = datetime.now()
      res = db.session.query(Show).filter_by(venue_id=self.id).filter(Show.start_time > currentDateTime).all()
      return res
    @hybrid_property
    def past_shows_count(self):
      currentDateTime = datetime.now()
      return db.session.query(Show).filter_by(venue_id=self.id).filter(Show.start_time < currentDateTime).count()
    @hybrid_property
    def upcoming_shows_count(self):
      currentDateTime = datetime.utcnow()
      return db.session.query(Show).filter_by(venue_id=self.id).filter(Show.start_time > currentDateTime).count()
    '''
    @upcoming_shows_count.expression
    def upcoming_shows_count(cls):
      currentDateTime = datetime.utcnow()
      return select(func.count(Show.id))
      #return db.session.query(Show).filter_by(venue_id=cls.id).filter(Show.start_time > currentDateTime).count()
    '''


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    @hybrid_property
    def past_shows(self):
      currentDateTime = datetime.now()
      res = db.session.query(Show).filter_by(artist_id=self.id).filter(Show.start_time < currentDateTime).all()
      return res
    @hybrid_property
    def upcoming_shows(self):
      currentDateTime = datetime.now()
      res = db.session.query(Show).filter_by(artist_id=self.id).filter(Show.start_time > currentDateTime).all()
      return res
    @hybrid_property
    def past_shows_count(self):
      currentDateTime = datetime.now()
      return db.session.query(Show).filter_by(artist_id=self.id).filter(Show.start_time < currentDateTime).count()
    @hybrid_property
    def upcoming_shows_count(self):
      currentDateTime = datetime.now()
      return db.session.query(Show).filter_by(artist_id=self.id).filter(Show.start_time > currentDateTime).count()


class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time = db.Column(db.DateTime, nullable=False)
  @hybrid_property
  def artist_name(self):
    return db.session.query(Artist).filter_by(id=self.artist_id).first().name
  @hybrid_property
  def artist_image_link(self):
    return db.session.query(Artist).filter_by(id=self.artist_id).first().image_link
  @hybrid_property
  def venue_name(self):
    return db.session.query(Venue).filter_by(id=self.venue_id).first().name
  @hybrid_property
  def venue_image_link(self):
    return db.session.query(Venue).filter_by(id=self.venue_id).first().image_link

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  city_state = db.session.query(Venue.city, Venue.state).group_by(Venue.city,Venue.state).all()
  data = []
  for res in city_state:
    data_tmp = {}
    data_tmp['city'] = res.city
    data_tmp['state'] = res.state
    data_tmp['venues'] = []
    venues = db.session.query(Venue.id, Venue.name).filter_by(city=res.city).filter_by(state=res.state).all()
    currentDateTime = datetime.utcnow()
    for v in venues:
      data_tmp['venues'].append({
        "id":v.id,
        "name":v.name,
        "num_upcoming_shows":Venue.query.filter_by(id=v.id).first().upcoming_shows_count
      })
    if len(data_tmp['venues']) != 0:
      data.append(data_tmp)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  word = request.form.get('search_term', '')
  res = db.session.query(Venue).filter(Venue.name.like('%'+ word +'%')).all()
  response = {
    "count": len(res),
    "data": []
  }
  for r in res:
    response['data'].append({
      "id": r.id,
      "name": r.name,
      "num_upcoming_shows": Venue.query.filter_by(id=r.id).first().upcoming_shows_count
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.filter_by(id=venue_id).first()
  db.session.expunge(data)
  data.genres = data.genres.split(",")
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    print(request.form)
    v = Venue(name=request.form['name'], city=request.form['city'], 
      state=request.form['state'], address=request.form['address'], phone=request.form['phone'], 
      image_link=request.form['image_link'], 
      facebook_link=request.form['facebook_link'], 
      website=request.form['website_link'], 
      seeking_talent=(request.form.get('seeking_talent', default='n')=='y'), seeking_description=request.form['seeking_description'],
      genres=','.join(request.form.getlist('genres')))
    db.session.add(v)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    error = True
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  db.query(Show).filter(Show.venue_id==venue_id).delete()
  db.query(Venue).filter(Venue.id==venue_id).delete()
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  word = request.form.get('search_term', '')
  res = db.session.query(Artist).filter(Artist.name.like('%'+ word +'%')).all()
  response = {
    "count": len(res),
    "data": []
  }
  for r in res:
    response['data'].append({
      "id": r.id,
      "name": r.name,
      "num_upcoming_shows": Artist.query.filter_by(id=r.id).first().upcoming_shows_count
    })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.filter_by(id=artist_id).first()
  db.session.expunge(data)
  data.genres = data.genres.split(",")
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    print(request.form)
    a = Artist.query.filter_by(id=artist_id).first()
    a.name = request.form['name']
    a.city = request.form['city']
    a.state = request.form['state']
    a.phone = request.form['phone']
    a.image_link = request.form['image_link']
    a.facebook_link = request.form['facebook_link']
    a.website = request.form['website_link']
    a.seeking_venue = request.form.get('seeking_venue', default='n')=='y'
    a.seeking_description = request.form['seeking_description']
    a.genres = ','.join(request.form.getlist('genres'))
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except Exception as e:
    print(e)
    error = True
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    print(request.form)
    v = Venue.query.filter_by(id=venue_id).first()
    v.name = request.form['name']
    v.city = request.form['city']
    v.address = request.form['address']
    v.state = request.form['state']
    v.phone = request.form['phone']
    v.image_link = request.form['image_link']
    v.facebook_link = request.form['facebook_link']
    v.website = request.form['website_link']
    v.seeking_talent = request.form.get('seeking_talent', default='n')=='y'
    v.seeking_description = request.form['seeking_description']
    v.genres = ','.join(request.form.getlist('genres'))
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  except Exception as e:
    print(e)
    error = True
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    print(request.form)
    a = Artist(name=request.form['name'], city=request.form['city'], 
      state=request.form['state'], phone=request.form['phone'], 
      image_link=request.form['image_link'], 
      facebook_link=request.form['facebook_link'], 
      website=request.form['website_link'], 
      seeking_venue=(request.form.get('seeking_venue', default='n')=='y'), seeking_description=request.form['seeking_description'],
      genres=','.join(request.form.getlist('genres')))
    db.session.add(a)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    error = True
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = db.session.query(Show).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    print(request.form)
    s = Show(venue_id=request.form['venue_id'], 
      artist_id=request.form['artist_id'], 
      start_time=request.form['start_time'])
    db.session.add(s)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    error = True
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
