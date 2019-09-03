from flask import Blueprint, render_template, url_for, request, flash, redirect,session, abort
from models.user import User
from models.image import Image
from models.transaction import Transaction
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from helpers.upload import upload as img_upload
from helpers.donate import generate_client_token, find_transaction, transact,TRANSACTION_SUCCESS_STATUSES
from helpers.email import send_email

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
    flash("Wrong password or username",'error')
    return redirect(url_for('users.login_form'))
            
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@users_blueprint.route('/<user_id>/profile', methods=["GET"])
@login_required
def profile(user_id):
    user_id = User.get_by_id(user_id)
    return render_template('users/profile.html', user_id=user_id)


@users_blueprint.route('/<username>', methods=["GET"])
def view(username):
    user = User.get_or_none(User.username == username)
    images = Image.select().where(Image.user_id == user.id)
    return render_template('users/view.html', user=user, images=images)

@users_blueprint.route('/search', methods=["POST"])
def show():
    name_input = request.form['username']
    username = User.get_or_none(User.username == name_input)
    if username:
        return redirect(url_for('users.view', username=name_input))
    else:
        return abort(404)


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return "USERS"


@users_blueprint.route('/<user_id>/edit', methods=['GET'])
@login_required
def edit(user_id):
    user = User.get_by_id(user_id)
    if current_user == user:
        return render_template('users/edit.html', user_id=user_id)
    else:
        flash('WRONG ACCOUNT')
        return redirect(url_for('users.profile', user_id=user_id))

@users_blueprint.route('/<user_id>/edit', methods=['POST'])
@login_required
def edit_form(user_id):
    user = User.get_by_id(user_id)
    username = request.form['username']
    email = request.form['email']
    if user.id == current_user.id:
        if user.username == username and user.email == email:
            flash("no information update needed" , 'success')
            return render_template('users/edit.html')
        else:
            user.username = username
            user.email = email
            if user.save():
                flash('Infomation Updated!' , 'success')
                return redirect(url_for('users.profile',user_id=user_id))
            else:
                flash('<br>'.join(user.errors),'error')
                return redirect(url_for('users.profile',user_id=user_id))
    flash('Something went wrong!' , 'error')
    # flash("Old password doesn't match", 'error')
    # return redirect(url_for('users.profile',user_id=user_id))

@users_blueprint.route('/<user_id>/password', methods=['GET'])
@login_required
def password(user_id):
    user = User.get_by_id(user_id)
    if current_user.id == user.id:
        return render_template('users/password.html', user_id=user_id)
    else:
        flash('WRONG ACCOUNT')
        return render_template('users/password.html', user_id=user_id)


@users_blueprint.route('/<user_id>/password', methods=['POST'])
@login_required
def edit_pw(user_id):
    user = User.get_by_id(user_id)
    password = request.form['password']
    new_password = request.form['new_password']
    confirm_pw = request.form['confirm_pw']
    if check_password_hash(user.password, password):
        if new_password == confirm_pw:
            user.password = new_password
            user.save()
            flash('Password Changed!' , 'success')
            return redirect(url_for('users.profile',user_id=user_id))
        flash('new password does not match confirm password' , 'error')
    flash("Old password doesn't match", 'error')
    return redirect(url_for('users.profile',user_id=user_id))


@users_blueprint.route('/<user_id>/imgupload', methods=['GET'])
@login_required
def upload_form(user_id):
    user = User.get_by_id(user_id)
    if current_user.id == user.id:
        return render_template('users/imgupload.html', user_id=user_id)

@users_blueprint.route('/<user_id>/imgupload', methods=['POST'])
@login_required
def upload(user_id):
    user = User.get_by_id(user_id)
    if current_user.id == user.id:
        img_upload("profileImg/")
        file = request.files.get('image').filename
        user.image = file
        user.save()
        flash("Profile image successfully uploaded" , "success")
        return redirect(url_for("users.profile", user_id=user_id))

@users_blueprint.route('/<user_id>/userimg', methods=['GET'])
@login_required
def userimg_form(user_id):
    user = User.get_by_id(user_id)
    if current_user.id == user.id:
        return render_template('users/userimage.html', user_id=user_id)

@users_blueprint.route('/<user_id>/userimg', methods=['POST'])
@login_required
def userimg(user_id):
    user = User.get_by_id(user_id)
    if current_user.id == user.id:
        img_upload("userImg/")
        file = request.files.get('image').filename
        image = Image(userImg=file, user_id = current_user.id)
        image.save()
        flash("Image successfully uploaded" , "success")
        return redirect(url_for("users.profile", user_id=user_id))

@users_blueprint.route('/donate/<img_id>', methods=['GET'])
@login_required
def donate_form(img_id):
    client_token = generate_client_token()
    return render_template('users/donate.html', client_token=client_token, img_id=img_id)

@users_blueprint.route('/show_donate/<transaction_id>', methods=['GET'])
def show_donate(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }

    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('users/show.html', transaction=transaction, result=result)


@users_blueprint.route('/donate/<img_id>', methods=['POST'])
@login_required
def donate(img_id):
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        flash('Donate successfully', 'success')
        image = Image.get_by_id(img_id)
        send_email(recipient=image.user.email, donor=current_user.email, amount=result.transaction.amount)
        Transaction(image_id=img_id, user_id=current_user.id, transaction_history=result.transaction.id, amount=result.transaction.amount).save()
        return redirect(url_for('users.show_donate',transaction_id=result.transaction.id))
    else:
        flash('Donate failed', 'error')
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message),'error')
        return redirect(url_for('users.donate_form',img_id=img_id))



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
    # return redirect(url_for('home'))