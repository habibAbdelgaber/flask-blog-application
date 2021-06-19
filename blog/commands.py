from blog.extensions import db
from blog.models import User, Post

import click
from flask.cli import with_appcontext


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()



