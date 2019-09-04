from app import app
from flask import render_template, abort
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from helpers.email import send_email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    # follower = current_user.id
    # follow = User_follower.get((User_follower.user==user) &( User_follower.follower==follower))
    # followers = current_user.id
    # following = User_follower.get((User_follower.user==users.id) &( User_follower.follower==followers))
    return render_template('home.html')
    # return abort(500)
