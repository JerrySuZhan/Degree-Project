import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/house_big?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0806@152.136.209.86:3306/house_big?charset=utf8'

    # 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PHOTO_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_image/photo')
    PHOTO_BUILDING_DIR = os.path.join(basedir, 'static/uploaded_image/building')

    DROPZONE_MAX_FILE_SIZE = 300
    DROPZONE_MAX_FILES = 3
    MAX_CONTENT_LENGTH = 300*1024*1024
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
