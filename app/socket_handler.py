from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from extensions import mongo, socketio

admin_socket_id = None

def register_socket_events(socketio):

    @socketio.on('connect')
    def handle_connect():
        global admin_socket_id
        user_id = request.args.get('user_id')
        role = request.args.get('role')
        if role == 'admin':
            admin_socket_id = request.sid
            print(f"Admin connected: {user_id} with socket_id: {admin_socket_id}")
