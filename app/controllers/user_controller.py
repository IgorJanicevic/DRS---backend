from flask import Blueprint,request
from services.user_service import UserService

user_routes = Blueprint('user_routes',__name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data['email'])
    return UserService.register_user(data)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return UserService.login_user(data)

@user_routes.route('/<user_id>', methods=['PUT'])
def update(user_id):
    data=  request.get_json()
    return UserService.update_profile(user_id,data)

@user_routes.route('/', methods=['GET'])
def get_all_users():
    return UserService.get_all_users()



