from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, DateField, PasswordField, BooleanField, SubmitField, validators, \
    FileField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import and_
from blogapp import db
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from wtforms import form, fields, validators, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    email = StringField(' ', validators=[DataRequired(message= u'Please enter your email'), Email(message= u'Please enter a valid email，e.g.：username@domain.com')])
    password = PasswordField(' ', validators=[DataRequired(message= u'Please enter your password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField(' ', validators=[DataRequired(message= u'Please enter your username')])
    email = StringField(' ', validators=[DataRequired(message= u'Please enter your email'), Email(message= u'Please enter a valid email，e.g.：username@domain.com')])
    password = PasswordField(' ', validators=[DataRequired(message= u'Please enter your password')])
    password2 = PasswordField(' ', validators=[DataRequired(message= u'Please enter your password twice')])
    submit = SubmitField('Sign up')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone = StringField('Phone')
    # email = StringField('Email', validators=[DataRequired()])
    district = SelectField('District', coerce=str,
                           choices=[('东城', 'Dongcheng'), ('西城', 'Xicheng'),
                                                                       ('朝阳', 'Chaoyang'), ('海淀', 'Haidian'),
                                                                       ('通州', 'Tongzhou'), ('昌平', 'Changping'),
                                                                       ('怀柔', 'Huairou'), ('密云', 'Miyun'),
                                                                       ('门头沟', 'Mentougou'), ('丰台', 'Fengtai'),
                                                                       ('石景山', 'Shijingshan'), ('房山', 'Fangshan'),
                                                                       ('顺义', 'Shunyi'), ('大兴', 'Daxing'),
                                                                       ('延庆', 'Yanqing'), ('平谷', 'Pinggu')
                                                                       ])    
    address = StringField('Address')
    photo = FileField('Photo', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(' ', validators=[DataRequired(message= u'Please enter your old password')])
    new_password = PasswordField(' ', validators=[DataRequired(message= u'Please enter your new password')])
    new_password2 = PasswordField(' ', validators=[DataRequired(message= u'Please enter your new password twice')])
    submit = SubmitField('Save Changes')

class AddHouseForm(FlaskForm):
    district = SelectField('District', validators=[DataRequired()], coerce=str, choices=[('东城', 'Dongcheng'), ('西城', 'Xicheng'),
                                                                       ('朝阳', 'Chaoyang'), ('海淀', 'Haidian'),
                                                                       ('通州', 'Tongzhou'), ('昌平', 'Changping'),
                                                                       ('怀柔', 'Huairou'), ('密云', 'Miyun'),
                                                                       ('门头沟', 'Mentougou'), ('丰台', 'Fengtai'),
                                                                       ('石景山', 'Shijingshan'), ('房山', 'Fangshan'),
                                                                       ('顺义', 'Shunyi'), ('大兴', 'Daxing'),
                                                                       ('延庆', 'Yanqing'), ('平谷', 'Pinggu')
                                                                       ])    
    address = StringField('Address', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    floor_range = SelectField('Floor Range', validators=[DataRequired()], coerce=str, choices=[('低楼层', 'Low Floor'), ('中楼层', 'Medium Floor'),
                                       ('高楼层', 'High Floor'), ('顶层', 'Top Floor'),
                                       ('底层', 'Ground Floor')
                                       ])
    floor_number = StringField('Floor Number', validators=[DataRequired()])
    bedroom_number = IntegerField('Bedroom Number', validators=[DataRequired()])
    livingroom_number = IntegerField('Living Room Number', validators=[DataRequired()])
    orientation = SelectField('Orientation', validators=[DataRequired()], coerce=str, choices=[('南', 'South'), ('北', 'North'),
                                                                                 ('东', 'East'), ('西', 'West'), ('西北', 'North West'), ('西南', 'South West'), ('东南', 'South East'), ('东北', 'North East')])
    year = IntegerField('Year', validators=[DataRequired()])
    detail = StringField('Detail')
    # photo = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    photo1 = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    photo2 = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    photo3 = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
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

class SendEmailForm(FlaskForm):
    emailaddress = StringField(' ', validators=[DataRequired(message= u'Please enter your email'), Email(message= u'Please enter a valid email，e.g.：username@domain.com')])
    submit = SubmitField('Send')

class VerifyAndResetForm(FlaskForm):
    v_code = StringField(' ', validators=[DataRequired(message= u'Please enter the verification code')])
    new_password = PasswordField(' ', validators=[DataRequired(message= u'Please enter your new password')])
    new_password2 = PasswordField(' ', validators=[DataRequired(message= u'Please enter your new password twice')])
    submit = SubmitField('Reset')

class SingleForm(FlaskForm):
    content=StringField(' ', validators=[DataRequired(message= u'Say something?')])
    submit = SubmitField('Send Message')

class EditForm(FlaskForm):
    district = SelectField('District', validators=[DataRequired()], coerce=str, choices=[('东城', 'Dongcheng'), ('西城', 'Xicheng'),
                                                                       ('朝阳', 'Chaoyang'), ('海淀', 'Haidian'),
                                                                       ('通州', 'Tongzhou'), ('昌平', 'Changping'),
                                                                       ('怀柔', 'Huairou'), ('密云', 'Miyun'),
                                                                       ('门头沟', 'Mentougou'), ('丰台', 'Fengtai'),
                                                                       ('石景山', 'Shijingshan'), ('房山', 'Fangshan'),
                                                                       ('顺义', 'Shunyi'), ('大兴', 'Daxing'),
                                                                       ('延庆', 'Yanqing'), ('平谷', 'Pinggu')
                                                                       ])    
    size = FloatField('Size', validators=[DataRequired()])
    orientation = SelectField('Orientation', validators=[DataRequired()], coerce=str, choices=[('南', 'South'), ('北', 'North'),
                                                                                 ('东', 'East'), ('西', 'West'), ('西北', 'North West'), ('西南', 'South West'), ('东南', 'South East'), ('东北', 'North East')])

    floor_range = SelectField('Floor Range', validators=[DataRequired()], coerce=str,
                              choices=[('低楼层', 'Low Floor'), ('中楼层', 'Medium Floor'),
                                       ('高楼层', 'High Floor'), ('顶层', 'Top Floor'),
                                       ('底层', 'Ground Floor')
                                       ])
    year = IntegerField('Year', validators=[DataRequired()])
    bedroom_number = IntegerField('Bedroom Number', validators=[DataRequired()])
    livingroom_number = IntegerField('Living Room Number', validators=[DataRequired()])
    floor_number = StringField('Floor Number', validators=[DataRequired()])
    total_price = FloatField('Total Price', validators=[DataRequired()])
    submit = SubmitField('Edit')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
