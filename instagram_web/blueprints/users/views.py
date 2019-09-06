from flask import Blueprint, render_template, url_for, request, flash, redirect,session, abort, jsonify
from models.user import User
from models.image import Image
from models.user_follower import User_follower
from models.transaction import Transaction
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from helpers.upload import upload as img_upload
from helpers.donate import generate_client_token, find_transaction, transact,TRANSACTION_SUCCESS_STATUSES
from helpers.email import send_email, follower_email
from helpers.google_oauth import oauth

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

@users_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('users.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@users_blueprint.route('/authorize')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash('Logged In','success')
        return redirect(url_for('users.profile',user_id=user.id))
    else:
        flash('Login Failed Please Sign Up', 'error')
        return redirect(url_for('users.new'))
        

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
    # followers = User_follower.user_id.followers.count()
    # following = User_follower.following.count()
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
    if username == current_user:
        return redirect(url_for('users.profile', user_id=current_user.id))
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
        flash('WRONG ACCOUNT', 'error')
        return redirect(url_for('users.profile', user_id=user_id))

@users_blueprint.route('/<user_id>/edit', methods=['POST'])
@login_required
def edit_form(user_id):
    user = User.get_by_id(user_id)
    username = request.form['username']
    email = request.form['email']
    privacy = request.form.get('privacy')
    if user.id == current_user.id:
        if user.username == username and user.email == email and user.is_private == privacy:
            flash("no information update needed" , 'success')
            return render_template('users/edit.html')
        else:
            user.username = username
            user.email = email
            user.is_private = privacy
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

# @users_blueprint.route('/<user_id>/<username>/follow', methods=['POST'])
# @login_required
# def follow(user_id, username):
#     user = User.get_by_id(user_id)
#     followers = current_user.id
#     following = User_follower(user_id=user.id, follower=followers).save()
#     flash('Follow successfully!' , 'success')
#     return redirect(url_for('users.view',user_id=user_id, username=username))

@users_blueprint.route('/<user_id>/<username>/follow', methods=['GET'])
@login_required
def follow(user_id, username):
    user = User.get_by_id(user_id)
    follower = current_user.id
    if user.is_private == True:
        follower_email(user=user.email,f_username = current_user.username, follower=current_user.email)
        following = User_follower(user_id = user.id, follower=follower, is_approved=False).save()
        response = {
            "status": "success",
            "new_follower_count": len(user.followers),
            "privacy": user.is_private
        }
        return jsonify(response)

    else:
        following = User_follower(user_id = user.id, follower=follower, is_approved=True).save()
        response = {
            "status": "success",
            "new_follower_count": len(user.followers),
            "privacy": user.is_private

        }
        return jsonify(response)
        


@users_blueprint.route('/<user_id>/<username>/unfollow', methods=['GET'])
@login_required
def unfollow(user_id, username):
    user = User.get_by_id(user_id)
    followers = current_user.id
    following = User_follower.get((User_follower.user==user.id) &( User_follower.follower==followers))
    # User_follower.get((User_follower.user_id == 34) & (User_follower.follower_id == 32))
    following.delete_instance()
    # flash('Unfollow successfully!' , 'success')
    response = {
        "status": "success",
        "new_follower_count": len(user.followers)
    }
    return jsonify(response)


@users_blueprint.route('/<following_id>/approval')
@login_required
def approval(following_id):
    following = User_follower.get((User_follower.user==current_user.id) &( User_follower.follower==following_id))
    following.is_approved = True
    following.save()
    
    response = {
        "status": "success",
        "new_follower_count": len(current_user.followers),
        "new_follower_requests_count": len(current_user.follower_requests)
    }
    return jsonify(response)


@users_blueprint.route('/<following_id>/decline')
@login_required
def decline(following_id):
    following = User_follower.get((User_follower.user==current_user.id) &( User_follower.follower==following_id))
    following.is_approved = True
    following.delete_instance()
    # return redirect(url_for("users.profile", user_id=following_id))
    response = {
        "status": "success",
        "new_follower_count": len(current_user.followers),
        "new_follower_requests_count": len(current_user.follower_requests)
    }
    return jsonify(response)




# @users_blueprint.route('/<user_id>/<username>/unfollow', methods=['POST'])
# @login_required
# def unfollow(user_id, username):
#     user = User.get_by_id(user_id)
#     followers = current_user.id
#     following = User_follower.get((User_follower.user==user.id) &( User_follower.follower==followers))
#     # User_follower.get((User_follower.user_id == 34) & (User_follower.follower_id == 32))
#     following.delete_instance()
#     flash('Unfollow successfully!' , 'success')
#     return redirect(url_for('users.view',user_id=user_id, username=username))

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