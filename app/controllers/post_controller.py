from flask import Blueprint,request
from services.post_service import PostService

post_routes = Blueprint('post_routes',__name__)

@post_routes.route('/',methods=['POST'])
def create():
    data = request.get_json()
    return PostService.create_post(data)

@post_routes.route('/<post_id>',methods=['PUT'])
def update(post_id):
    data = request.get_json()
    return PostService.update_post(post_id,data)

@post_routes.route('/<post_id>',methods=['DELETE'])
def delete(post_id):
    return PostService.delete_post(post_id)

@post_routes.route('/user/<user_id>',methods=['GET'])
def get_user_posts(user_id):
    return PostService.get_user_posts(user_id)