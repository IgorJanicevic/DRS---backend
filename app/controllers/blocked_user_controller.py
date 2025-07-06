from flask import Blueprint, request, jsonify
from services.blocked_user_service import BlockedUserService

blocked_user_routes = Blueprint('blocked_user_routes', __name__)

@blocked_user_routes.route('/', methods=['GET'])
def get_all_blocked_users():
    result=  BlockedUserService.get_all_blocked_users()
    return jsonify(result)



@blocked_user_routes.route('/<user_id>', methods=['DELETE'])
def unblock_user(user_id):
    return BlockedUserService.unblock_user(user_id)
