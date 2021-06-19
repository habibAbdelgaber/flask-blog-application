import os

ENV = 'env'
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if ENV == 'env':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # do something
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    debug = os.environ.get('debug')
    MAIL_SERVER = os.environ.get('EMAIL_SERVER')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')