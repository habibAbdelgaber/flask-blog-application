import os

ENV = 'env'
# class Config(object):
SECRET_KEY = os.environ.get('SECRET_KEY')
if ENV == 'env':
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    debug = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://bihnkfojpagzyr:9d75b34e093a2129f2bf3c209eafde2b1a20f950aedcdbc198ee7c1c4302c351@ec2-35-170-85-206.compute-1.amazonaws.com:5432/d2v5ccb96j6f2i')
    
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
debug = os.environ.get('debug')
MAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
