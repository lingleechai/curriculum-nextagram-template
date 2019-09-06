from flask import Blueprint, request, jsonify
from models.image import Image
from models.user import User


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    # order follow by alphabet
    users = User.select()
    response = {
    "id" : [user.id for user in users],
    "email" : [user.email for user in users],
    "username" : [user.username for user in users]
    }
    return jsonify(response)
    # return "USERS API"

@users_api_blueprint.route('/images/', methods=['GET'])
def image():
    images = Image.select().where(Image.user_id == request.args.get('userId'))
    user = User.get_by_id(request.args.get('userId'))
    response = {
        "user" : user.username,
        "images":["https://linglee-nextagram.s3-ap-southeast-1.amazonaws.com/userImg/" + image.userImg for image in images]
    }
    return jsonify(response)



# @users_api_blueprint.route('/login/', methods=['POST'])
# def login():
#     users = User.select()
#     response ={
#     "username" : [user.username for user in users],
#     "password" : [user.password for user in users]
#     }
#     return jsonify(response)