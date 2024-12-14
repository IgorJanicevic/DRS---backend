from flask import Blueprint,request
from services.friendship_service import FriendshipService

friendship_routes = Blueprint('friendship_routes',__name__)

@friendship_routes.route('/',methods=['POST'])
def create():
    data = request.get_json()
    return FriendshipService.create_friendship(data)

@friendship_routes.route('/<friendship_id>', methods=['PUT'])
def update_friendship(friendship_id):
    data = request.get_json()
    if not data:
        return {"message": "Invalid input"}, 400
    return FriendshipService.update_friendship(friendship_id, data)

@friendship_routes.route('/<friendship_id>/accept', methods=['PUT'])
def accept_friendship(friendship_id):
    return FriendshipService.update_friendship(friendship_id, {"status": "Accepted"})

@friendship_routes.route('/<friendship_id>/reject', methods=['PUT'])
def reject_friendship(friendship_id):
    return FriendshipService.update_friendship(friendship_id, {"status": "Rejected"})

@friendship_routes.route('/friends/<user_id>',methods=['GET'])
def get_friends(user_id):
    return FriendshipService.get_all_friends_ids(user_id)


@friendship_routes.route('/status/<user_id>/<friend_id>', methods=['GET'])
def get_friend_status(user_id,friend_id):
    ret_val =  FriendshipService.get_friendship_status(user_id,friend_id)
    return {'message':ret_val},200

        
