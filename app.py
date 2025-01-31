import os
import config
from models.user import User
from flask import Flask , render_template,redirect, flash, url_for
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask_login import LoginManager
from authlib.flask.client import OAuth

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
oauth = OAuth()
oauth.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
    # User.get_or_non(user_id == User.id)
@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in to continue!",'success')
    return redirect(url_for('users.login'))