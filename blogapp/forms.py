from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, DateField, PasswordField, BooleanField, SubmitField, validators, \
    FileField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import and_
from blogapp import db
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from wtforms import form, fields, validators, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    email = StringField(' ', validators=[DataRequired()])
    password = PasswordField(' ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField(' ', validators=[DataRequired()])
    email = StringField(' ', validators=[DataRequired()])
    password = PasswordField(' ', validators=[DataRequired()])
    password2 = PasswordField(' ', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    # district = SelectField('District', validators=[DataRequired()], choices=['Haidian', 'Chaoyang', 'Fengtai', 'Mentougou', 'Shijingshan', 'Fangshan', 'Tongzhou', 'Shunyi', 'Changping', 'Daxing', 'Huairou', 'Pinggu', 'Yanqing', 'Miyun', 'Xicheng','Dongcheng'])
    district = SelectField('District', validators=[DataRequired()], coerce=str,
                           choices=[('Dongcheng', 'Dongcheng'), ('Xicheng', 'Xicheng'),
                                    ('Chaoyang', 'Chaoyang'), ('Haidian', 'Haidian'),
                                    ('Tongzhou', 'Tongzhou'), ('Changping', 'Changping'),
                                    ('Huairou', 'Huairou'), ('Miyun', 'Miyun'),
                                    ('Mentougou', 'Mentougou'), ('Fengtai', 'Fengtai'),
                                    ('Shijingshan', 'Shijingshan'), ('Fangshan', 'Fangshan'),
                                    ('Shunyi', 'Shunyi'), ('Daxing', 'Daxing'),
                                    ('Yanqing', 'Yanqing'), ('Pinggu', 'Pinggu')
                                    ])
    address = StringField('Address', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(' ', validators=[DataRequired()])
    new_password = PasswordField(' ', validators=[DataRequired()])
    new_password2 = PasswordField(' ', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class AddHouseForm(FlaskForm):
    district = SelectField('District', validators=[DataRequired()], coerce=str, choices=[('Dongcheng', 'Dongcheng'), ('Xicheng', 'Xicheng'),
                                                                           ('Chaoyang', 'Chaoyang'), ('Haidian', 'Haidian'),
                                                                           ('Tongzhou', 'Tongzhou'), ('Changping', 'Changping'),
                                                                           ('Huairou', 'Huairou'), ('Miyun', 'Miyun'),
                                                                           ('Mentougou', 'Mentougou'), ('Fengtai', 'Fengtai'),
                                                                           ('Shijingshan', 'Shijingshan'), ('Fangshan', 'Fangshan'),
                                                                           ('Shunyi', 'Shunyi'), ('Daxing', 'Daxing'),
                                                                           ('Yanqing', 'Yanqing'), ('Pinggu', 'Pinggu')
                                                                           ])
    address = StringField('Address', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    floor_range = SelectField('Floor Range', validators=[DataRequired()], coerce=str, choices=[('Ground', 'Ground'), ('Low', 'Low'),
                                                                                 ('Medium', 'Medium'), ('High', 'High'),
                                                                                 ('Top', 'Top')
                                                                                 ])
    floor_number = StringField('Floor Number', validators=[DataRequired()])
    bedroom_number = IntegerField('Bedroom Number', validators=[DataRequired()])
    livingroom_number = IntegerField('Living Room Number', validators=[DataRequired()])
    orientation = SelectField('Orientation', validators=[DataRequired()], coerce=str, choices=[('North', 'North'), ('South', 'South'),
                                                                                 ('East', 'East'), ('West', 'West')])
    year = IntegerField('Year', validators=[DataRequired()])
    total_price = IntegerField('Total Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

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