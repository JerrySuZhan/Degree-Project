# -*- coding: utf-8 -*-
from datetime import datetime, date
from . import app
from . import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


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

    # def __repr__(self):
    #     return '<User %r>' % self.username



