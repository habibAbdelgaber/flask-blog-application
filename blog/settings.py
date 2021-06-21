import os

# ENV = 'env'
# # class Config(object):
# SECRET_KEY = os.environ.get('SECRET_KEY')
# if ENV == 'env':
#     debug = os.environ.get('debug')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# else:
#     debug = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://iiamjzfoyjyfzv:4fe9d4d61feaf1472d3bcbe22e71a5c5480bbdd7907f8f0c0276366a902c96cd@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d9pru0dgmgik21')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  
SQLALCHEMY_TRACK_MODIFICATIONS = False
# DEBUG = os.environ.get('DEBUG')
MAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')

# set FLASK_APP=/path/to/automain.py
# DATABASE_URL='sqlite:///sqlite3'
# SECRET_KEY='aff08866d4fcc1a574f0231f6ed0c14d'
# EMAIL_SERVER='smtp.googlemail.com'
# EMAIL_PORT=587
# EMAIL_USERNAME='youremail@gmail.com'
# EMAIL_PASSWORD='youremailpassword'
# EMAIL_USE_TLS=True
# EMAIL_USE_SSL=False
