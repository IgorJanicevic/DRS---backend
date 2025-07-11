from flask import Blueprint,request
from services.post_service import PostService
from datetime import datetime

post_routes = Blueprint('post_routes',__name__)

@post_routes.route('/create',methods=['POST'])
def create():
    print("Creating post...")
    data = request.get_json()
    ret_val=  PostService.create_post(data)
    return ret_val

@post_routes.route('/<post_id>',methods=['PUT'])
def update(post_id):
    data = request.get_json()
    data['timestamp'] = datetime.now()
    return PostService.update_post(post_id,data,'update')

@post_routes.route('/accept/<post_id>',methods=['PUT'])
def accept_post(post_id):
    return PostService.update_post(post_id,{'status':'Accepted'},'accept')

@post_routes.route('/reject/<post_id>',methods=['PUT'])
def reject_post(post_id):
    result = PostService.update_post(post_id,{'status':'Rejected'},'reject')
    return result

@post_routes.route('/<post_id>',methods=['DELETE'])
def delete(post_id):
    return PostService.delete_post(post_id)

@post_routes.route('/user/<user_id>',methods=['GET'])
def get_user_posts(user_id):
    return PostService.get_user_posts(user_id)

@post_routes.route('/pending',methods=['GET'])
def get_pending_posts():
    return PostService.get_pending_posts()

@post_routes.route('/<post_id>',methods=['GET'])
def get_post_by_id(post_id):
    return PostService.get_post_by_id(post_id)

@post_routes.route('/friends/<user_id>',methods=['GET'])
def get_friends_posts(user_id):
    return PostService.get_friends_posts(user_id)