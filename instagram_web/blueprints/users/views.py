from flask import Blueprint, render_template, url_for, request, flash, redirect,session
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash


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
def login_form():
    return render_template('users/login.html')

@users_blueprint.route('/login', methods=['POST'])
def login():
    users = User.select()
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and check_password_hash(user.password , password):
            login_user(user)
            flash("You are logged in",'success')
            return redirect(url_for('users.profile',user_id=user.id))
    flash("Something went wrong! please try again",'error')
    return redirect(url_for('users.login_form'))
            
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@users_blueprint.route('/<user_id>/profile', methods=["GET"])
@login_required
def profile(user_id):
    # breakpoint()
    user_id = User.get_by_id(user_id)
    return render_template('users/profile.html', user_id=user_id)

# @users_blueprint.route('/profile', methods=["GET"])
# @login_required
# def profile_ori():
#     return render_template('users/profile.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

# MANUAL LOGIN & LOGOUT
# @users_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         flash('Login sucessful !' , 'success')
#         return redirect(url_for('home'))
#     return render_template('users/login.html')


# @users_blueprint.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     flash('You are logged out!' , 'success')
#     return redirect(url_for('home'))