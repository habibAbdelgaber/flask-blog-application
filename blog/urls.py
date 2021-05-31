import secrets
import os
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, abort
from blog import app

from blog import app, db, bcrypt, User, Post
from blog.forms import SignupForm, SigninForm, UpdateProfileForm, PostForm
from flask_login import current_user, login_required, logout_user, login_user
from wtforms.validators import ValidationError

@app.route('/', methods=['GET'])
def home():
    posts = Post.query.all()
    return render_template('blog/home.html', posts=posts)

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
        flash(f'Hi, {user.username} welcome back!', category='success')
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

def picture(image_form):
    # 1- generate hash
    gen_token_hex = secrets.token_hex(10)
    print(gen_token_hex)
    # 2- find filename and extension, Hint! use os module
    file_name, file_ext = os.path.splitext(image_form.filename)
    # 3- concat generated hash to pic
    image_fn = gen_token_hex + file_ext
    # 4- store the image to the folder of images
    image_path = os.path.join(app.root_path, 'static/images', image_fn)
    # 5- rezise image Hint! use thumbnail method
    i_size = (100, 100)
    i = Image.open(image_form)
    i.thumbnail(i_size)
    i.save(image_path)
    # 6- save the image
    # image_path.save(image_form)
    # # 7- return filename
    return image_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.img.data:
            # print(picture('text'))
            image = picture(form.img.data)
            current_user.image = image
        current_user.username = form.username.data
        current_user.email  = form.email.data
        db.session.commit()
        flash('You have updated your account successfully!', category='success')
        return redirect(url_for('account'))
    elif request.method== 'GET':
        form.img.data = current_user.image
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='images/' + current_user.image)
    return render_template('registration/account.html', title='My account', image=image, form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have created a new post', category='success')
        return redirect(url_for('home'))
    return render_template('blog/create.html',title='New Post', legend='New Post', form=form)

@app.route('/detail/<int:id>', methods=['GET'])
def detail(id):
    post = Post.query.get(id)
    return render_template('blog/detail.html', title=post.title, post=post)



@app.route('/detail/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You have updated the post!', category='success')
        return redirect(url_for('detail', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blog/create.html', title='Update Post', post=post.id, legend='Upadet Post', form=form)

@app.route('/detail/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have deleted the post!', category='success')
    return redirect(url_for('home'))

# Assignment
"""
In this view we are going to write a logic that when users
click on Author's name will take them to that Author's entire posts page.
1- Create a simple function or route that does these logics:
a) Filter User by its username.
b) Filter Post by its Author
c) Render template that displays specific Author's posts.
2- From home page where all posts are displaying, add a url link that leads to that Author's posts page!. 
"""
