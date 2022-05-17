import sys
import babel
import logging
import dateutil.parser
import datetime
from datetime import datetime
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from forms import VenueForm, ArtistForm, ShowForm
from flask import Flask, render_template, request, flash, redirect, \
  url_for, abort
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
CsrfProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(
      db.DateTime,
      nullable=False,
    )

    # Venue
    venue = db.relationship('Venue')
    venue_id = db.Column(
      db.Integer,
      db.ForeignKey('venues.id', ondelete='CASCADE'),
      nullable=False,
    )

    # Artist
    artist = db.relationship('Artist')
    artist_id = db.Column(
      db.Integer,
      db.ForeignKey('artists.id', ondelete='CASCADE'),
      nullable=False,
    )

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    created_date = db.Column(db.DateTime)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show')
    artists = db.relationship(
        'Artist',
        secondary='shows',
        back_populates='venues'
    )


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show')
    venues = db.relationship(
        'Venue',
        secondary='shows',
        back_populates='artists'
    )