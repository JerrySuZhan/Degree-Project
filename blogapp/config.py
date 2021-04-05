import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0806@localhost:3306/house_small?charset=utf8'
    # 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PHOTO_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_image/photo')
