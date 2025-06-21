from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from extensions import mongo, socketio

post_routes = Blueprint('post_routes', __name__)

admin_socket_id = None

@socketio.on('connect')
def handle_connect():
    global admin_socket_id
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    if role == 'admin':
        admin_socket_id = request.sid
        print(f"Admin connected: {user_id} with socket_id: {admin_socket_id}")

@post_routes.route('/create', methods=['POST'])
def create_post():
    data = request.get_json()
    user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
    if user:
        data['username'] = user['username']
        post_data = {
            "user_id": data['user_id'],
            "username": data['username'],
            "description": data['description'],
            "timestamp": datetime.now(),
            "type": data['type'],
            "status": "Pending",
            "image_url": data['image_url']
        }
        result = mongo.db.posts.insert_one(post_data)
        post_data['_id'] = str(result.inserted_id)
        post_data['timestamp'] = str(post_data['timestamp'])
        socketio.emit('new_post', post_data, room=admin_socket_id)
        return post_data, 201
    return jsonify({"message": "User not found"}), 404
