from flask import Flask
from flask_mail import Mail, Message
from blogapp.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, use_native_unicode='utf8')

app.config['MAIL_SERVER'] = "smtp.126.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "zhangmengyi1999@126.com"
app.config['MAIL_PASSWORD'] = "PHZFGVPUPKNFBHZO"
app.config['MAIL_DEFAULT_SENDER'] = '1186273992@qq.com'
mail = Mail(app)

from blogapp import routes, models

from . import models
