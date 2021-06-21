from flask import render_template, Blueprint, request
# from blog import Post
# from blog import db
from blog.models import Post
main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=3) # displaying the posts in descending order
    return render_template('blog/home.html', posts=posts)

