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
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone = StringField('Phone')
    # email = StringField('Email', validators=[DataRequired()])
    district = SelectField('District', coerce=str,
                           choices=[('东城', '东城'), ('西城', '西城'),
                                    ('朝阳', '朝阳'), ('海淀', '海淀'),
                                    ('通州', '通州'), ('昌平', '昌平'),
                                    ('怀柔', '怀柔'), ('密云', '密云'),
                                    ('门头沟', '门头沟'), ('丰台', '丰台'),
                                    ('石景山', '石景山'), ('房山', '房山'),
                                    ('顺义', '顺义'), ('大兴', '大兴'),
                                    ('延庆', '延庆'), ('平谷', '平谷')
                                    ])
    address = StringField('Address')
    photo = FileField('Photo', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(' ', validators=[DataRequired()])
    new_password = PasswordField(' ', validators=[DataRequired()])
    new_password2 = PasswordField(' ', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class AddHouseForm(FlaskForm):
    district = SelectField('District', validators=[DataRequired()], coerce=str, choices=[('东城', '东城'), ('西城', '西城'),
                                                                           ('朝阳', '朝阳'), ('海淀', '海淀'),
                                                                           ('通州', '通州'), ('昌平', '昌平'),
                                                                           ('怀柔', '怀柔'), ('密云', '密云'),
                                                                           ('门头沟', '门头沟'), ('丰台', '丰台'),
                                                                           ('石景山', '石景山'), ('房山', '房山'),
                                                                           ('顺义', '顺义'), ('大兴', '大兴'),
                                                                           ('延庆', '延庆'), ('平谷', '平谷')
                                                                           ])
    address = StringField('Address', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    floor_range = SelectField('Floor Range', validators=[DataRequired()], coerce=str, choices=[('低楼层', '低楼层'), ('中楼层', '中楼层'),
                                                                                 ('高楼层', '高楼层'), ('顶层', '顶层'),
                                                                                 ('底层', '底层')
                                                                                 ])
    floor_number = StringField('Floor Number', validators=[DataRequired()])
    bedroom_number = IntegerField('Bedroom Number', validators=[DataRequired()])
    livingroom_number = IntegerField('Living Room Number', validators=[DataRequired()])
    orientation = SelectField('Orientation', validators=[DataRequired()], coerce=str, choices=[('南', '南'), ('北', '北'),
                                                                                 ('东', '东'), ('西', '西'), ('西北', '西北'), ('西南', '西南'), ('东南', '东南'), ('东北', '东北')])
    year = IntegerField('Year', validators=[DataRequired()])
    detail = StringField('Detail')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
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
    emailaddress = StringField(' ', validators=[DataRequired()])
    submit = SubmitField('Send')

class VerifyAndResetForm(FlaskForm):
    v_code = StringField(' ', validators=[DataRequired()])
    new_password = PasswordField(' ', validators=[DataRequired()])
    new_password2 = PasswordField(' ', validators=[DataRequired()])
    submit = SubmitField('Reset')

class SingleForm(FlaskForm):
    content=StringField(' ', validators=[DataRequired()])
    submit = SubmitField('Send Message')

