import os

from app import app


class BaseConfig():
    BASEDIR = app.root_path
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    WTF_CSRF_ENABLED = True
    DEBUG = False
    TESTING = False
