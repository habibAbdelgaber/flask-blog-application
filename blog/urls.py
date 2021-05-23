import secrets
import os
from flask import render_template, url_for, request, redirect, flash
from blog import app

from blog import app, db, bcrypt, User, Post
from blog.forms import SignupForm, SigninForm, UpdateProfileForm
from flask_login import current_user, login_required, logout_user, login_user
from wtforms.validators import ValidationError

@app.route('/', methods=['GET'])
def home():
     return render_template('blog/home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'You have signed up as {form.username.data } successfully', category='success')
        return redirect(url_for('signin'))
    return render_template('registration/signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SigninForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, form.remember.data)
        flash(f'Welcome back!', category='success')
        next_page = request.args.get('next')
        # if next_page:
        #     return redirect(url_for('account'))
        # else:
        #     return redirect(url_for('home'))
        return redirect(next_page) if next_page else redirect(url_for('home'))
    # else:
    #     flash('Invalid Username/Password!', category='danger')
    return render_template('registration/signin.html', form=form)


@app.route('/signout')
def logout():
    logout_user()
    flash('You have logged out successfuly!', category='success')
    return redirect(url_for('home'))

def picture(pic):
    # 1- generate hash
    # 2- assign generated hash to pic
    # 3- find filename and extension, Hint! use os module
    # 4- store the image to the folder of images
    # 5- rezise image Hint! use thumbnail method
    # 6- save the image
    # 7- return filename
    pass



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    image_file = url_for('static', filename='images/' + current_user.image)
    if form.validate_on_submit():
        if form.img.data:
            img = picture(image_file)
            form.img.data
        current_user.username = form.username.data
        current_user.email  = form.email.data
        db.session.commit()
        flash('You have updated your account successfully!', category='success')
        return redirect(url_for('account'))
    elif request.method== 'GET':
        form.img.data = current_user.image
        form.username.data = current_user.username
        form.email.data = current_user.email
      
    return render_template('blog/account.html', title='My account', image_file=image_file, form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # create a logic how to create a new posts
    return render_template('blog/create.html')



