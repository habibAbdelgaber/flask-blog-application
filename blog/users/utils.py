from PIL import Image
import os
import secrets
from flask import url_for, current_app
from blog.extensions import mail
from flask_mail import Message

def picture(image_form):
    # 1- generate hash
    gen_token_hex = secrets.token_hex(10)
    print(gen_token_hex)
    # 2- find filename and extension, Hint! use os module
    file_name, file_ext = os.path.splitext(image_form.filename)
    # 3- concat generated hash to pic
    image_fn = gen_token_hex + file_ext
    # 4- store the image to the folder of images
    image_path = os.path.join(current_app.root_path, 'static/images', image_fn)
    # 5- rezise image Hint! use thumbnail method
    i_size = (100, 100)
    i = Image.open(image_form)
    i.thumbnail(i_size)
    i.save(image_path)
    # 6- save the image
    # image_path.save(image_form)
    # # 7- return filename
    return image_fn


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset',sender='blog@blog.com', recipients=[user.email], body=f"""to reset your email password visit:
    {url_for('users.password_reset', token=token, _extrenal=True)}
    If you do not made this request, ignore it and no changes will be made!
    """)
    # msg.body(f"""to reset your email password visit:
    # {url_for('password_reset', token=token, _extrenal=True)}
    # If you do not made this request, ignore it and no changes will be made!
    # """)
    mail.connect()
    mail.send(msg)

