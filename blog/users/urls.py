from flask import render_template, url_for, request, redirect, flash, abort, Blueprint
from blog import mail
from blog.users.utils import picture, send_email
from blog import db, bcrypt
# from blog import db
from blog.models import Post, User
from blog.users.forms import(
    SignupForm, SigninForm, UpdateProfileForm,
    RequestPasswordForm, PasswordResetForm
    )
from flask_login import current_user, login_required, logout_user, login_user
from wtforms.validators import ValidationError
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignupForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'You have signed up as {form.username.data } successfully', category='success')
        return redirect(url_for('users.signin'))
    return render_template('registration/signup.html', form=form)

@users.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, form.remember.data)
        flash(f'Hi, {user.username} welcome back!', category='success')
        next_page = request.args.get('next')
        # if next_page:
        #     return redirect(url_for('users.account'))
        # else:
        #     return redirect(url_for('main.home'))
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    # else:
    #     flash('Invalid Username/Password!', category='danger')
    return render_template('registration/signin.html', form=form)


@users.route('/signout')
def logout():
    logout_user()
    flash('You have logged out successfuly!', category='success')
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method== 'GET':
        form.img.data = current_user.image
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='images/' + current_user.image)
    return render_template('registration/account.html', title='My account', image=image, form=form)




@users.route('/password_reset', methods=['GET', 'POST'])
def password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        # token = user.get_reset_token()
        # msg = Message('Password Reset',sender='blog@blog.com', recipients=[user.email])
        # msg.body(f"""to reset your email password visit: {url_for('password_reset', token=token, _extrenal=True)}
        # If you do not made this request, ignore it and no changes will be made!""")
        # mail.send(msg)
        send_email(user)
        flash('An email has been sent with an instructions to reset your password!', category='info')
        return redirect('main.home')
    return render_template('registration/password_request_email.html',  title='Request Password Reset', form=form)


@users.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect('main.home')

    user = User.request_token(token)
    if not user:
        flash('Your request time has been expired, please request again!', category='warning')
        return redirect(url_for('users.password_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password_hashed
        db.session.commit()
        flash(f'Your password has been reset successfully, you can login now', category='success')
        return redirect(url_for('users.signin'))

    return render_template('registration/password_reset.html', title='Password Reset', form=form)

        
