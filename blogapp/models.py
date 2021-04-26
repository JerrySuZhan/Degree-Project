# -*- coding: utf-8 -*-
from . import db

class Buildings(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    district = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    total_price = db.Column(db.Float, index=True)
    price_per_meter = db.Column(db.Float, index=True)
    build_time = db.Column(db.Integer, index=True)
    num_of_bedrooms = db.Column(db.Integer, index=True)
    num_of_living_rooms = db.Column(db.Integer, index=True)
    size = db.Column(db.Integer, index=True)
    orientation = db.Column(db.String(64), index=True)
    building_type = db.Column(db.String(64), index=True)
    num_of_floors = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    detail = db.Column(db.String(2000))
    photo = db.Column(db.String(256))
    message = db.relationship('Message', backref='buildings')

    # def __repr__(self):
    #     return '<User %r>' % self.username

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    district = db.Column(db.String(150))
    address = db.Column(db.String(1200))
    photo = db.Column(db.String(256))
    buildings = db.relationship('Buildings', backref='user')
    message = db.relationship('Message', backref='user')

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    house_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    content = db.Column(db.String(1200))