from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, DateField, PasswordField, BooleanField, SubmitField, validators, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import and_
from blogapp import db
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from wtforms import form, fields, validators, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class search_buildings(FlaskForm):
    district = StringField("district")
    address = StringField("address")
    total_price = StringField("total_price")
    price_per_meter = StringField("price_per_meter")
    build_time = StringField("build_time")
    num_of_bedrooms = StringField("num_of_bedrooms")
    num_of_living_rooms = StringField("num_of_living_rooms")
    size = StringField("size")
    orientation = StringField("orientation")
    building_type = StringField("building_type")
    num_of_floors = StringField("num_of_floors")
    submit = SubmitField("SEARCH")

class search_conditions(FlaskForm):
    submit = SubmitField()