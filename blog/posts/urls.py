from flask import render_template, url_for, request, redirect, flash, abort, Blueprint
from blog import db
from blog.models import Post, User
from flask_login import login_required, current_user
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have created a new post', category='success')
        return redirect(url_for('main.home'))
    return render_template('blog/create.html',title='New Post', legend='New Post', form=form)

@posts.route('/detail/<int:id>', methods=['GET'])
def detail(id):
    post = Post.query.get(id)
    return render_template('blog/detail.html', title=post.title, post=post)



@posts.route('/detail/<int:id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.detail', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blog/create.html', title='Update Post', post=post.id, legend='Upadet Post', form=form)

@posts.route('/detail/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have deleted the post!', category='success')
    return redirect(url_for('main.home'))


# Assignment
# In this view we are going to write a logic that when users
# click on Author's name will take them to that Author's entire posts page.
# 1- Create a simple function or route that does these logics:
@posts.route('/user/posts/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # a) Filter User by its username.
    user = User.query.filter_by(username=username).first()
    # b) Filter Post by its Author
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_created.desc())\
    .paginate(page=page, per_page=3)
    # c) Render template that displays specific Author's posts.
    return render_template('blog/user_posts.html', title='user posts', user=user, posts=posts)
# 2- From home page where all posts are displaying, add a url link that leads to that Author's posts page!. 

