from flask import Blueprint, render_template, url_for, request, flash, redirect,session
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new_form', methods=['POST'])
def create():
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    comfirm_pw = request.form['confirm_pw']
    if password == comfirm_pw:
        user = User(email=email, username=username, name=name ,password=password)
        if user.save():
            flash('Sign Up Successful!','success')
            return redirect(url_for('users.new'))
        else:
            flash('<br>'.join(user.errors),'error')
            return render_template('users/new.html')
    else:
        flash('confirm password is not the same as password','error')
        return render_template('users/new.html')

@users_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('users/login.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
