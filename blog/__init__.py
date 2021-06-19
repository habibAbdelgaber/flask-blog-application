from .commands import create_tables
from flask import Flask
from .extensions import db, mail, bcrypt, login_manager
# from .settings import Config


def create_app(config_file='settings.py'):
# def create_app():
    app = Flask(__name__)
    with app.app_context():
        # init_db()
        app.config.from_pyfile(config_file)
        # app.config.from_object(Config)

        db.init_app(app)
        mail.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)

        app.cli.add_command(create_tables)

        from blog.main.urls import main
        from blog.posts.urls import posts
        from blog.users.urls import users
        from blog.errors.handlers import errors

        app.register_blueprint(main)
        app.register_blueprint(posts)
        app.register_blueprint(users)
        app.register_blueprint(errors)


    return app











