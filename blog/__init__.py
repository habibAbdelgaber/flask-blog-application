from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aff08866d4fcc1a574f0231f6ed0c14d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'


# app.config['EMAIL_SERVER'] = 'smtp.gmail.com'
# app.config['EMAIL_PORT'] = 587
# # app.config['EMAIL_PORT'] = 465
# app.config['EMAIL_USERNAME'] = ''
# app.config['EMAIL_PASSWORD'] = ''
# app.config['EMAIL_USE_TLS'] = False
# # app.config['EMAIL_USE_SSL'] = True

app.config.update(dict(
    debug=True,
    MAIL_SERVER = 'smtp.googlemail.com',
    EMAIL_PORT = 587,
    EMAIL_USERNAME = 'youremail@gmail.com',
    EMAIL_PASSWORD = 'youremailpassword',
    EMAIL_USE_TLS = True
))

mail = Mail(app)

from blog.main.urls import main
from blog.posts.urls import posts
from blog.users.urls import users

app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(users)












