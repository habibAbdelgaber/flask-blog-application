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

app.config['EMAIL_SERVER'] = 'smtp.googlemail.com'
app.config['EMAIL_PORT'] = 587
app.config['EMAIL_USE_TLS'] = True
app.config['EMAIL_USERNAME'] = ''
app.config['EMAIL_PASSWORD'] = ''


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'
mail = Mail(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(100), nullable=True, default='default.png')
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def request_reset(self, exp_sec=1200):
        """
        to demonstrate how itsdangerous package works follow the steps bellow:
        1- go to terminal or windows command line and type python to get into python's shell
        2- from python's shell do this: from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        3- to send secret token, do this in python's shell: s = Serializer('test', 30), test is token and 30 is expiration time.
        4- to generate secret token, token = s.dumps({'user_id': 1}).decode('utf-8')
        5- to check if secret token has been sent and generated, type: token + enter
        6- to find out if token has been expired, type: s.loads(token) + enter
        """
        s = Serializer(app.config['SECRET_KEY'], exp_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def request_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'{self.username}, {self.email}, {self.image}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.title}, {self.date_created}'


from blog import urls












