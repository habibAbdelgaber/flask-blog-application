import os

ENV = 'env'
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if ENV == 'env':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        debug = False
        SQLALCHEMY_DATABASE_URI = 'postgres://jltzdmyzzsimhy:2f8bf8e6a70719612d0f6c31de5720eec37b6d940e0abf0eeebffc6a7d451198@ec2-50-17-255-120.compute-1.amazonaws.com:5432/d3dc2rngdlrnp5'
       
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    debug = os.environ.get('debug')
    MAIL_SERVER = os.environ.get('EMAIL_SERVER')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
    