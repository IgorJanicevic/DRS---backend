from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService


notification_routes = Blueprint('notification_routes', __name__)

@notification_routes.route('/', methods=['POST'])
def create_notification():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    notification = NotificationService.create_notification(data)
    return jsonify(notification), 201

@notification_routes.route('/<notification_id>', methods=['PUT'])
def update_notification(notification_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    updated_notification = NotificationService.update_notification(notification_id, data)
    return jsonify(updated_notification), 200

@notification_routes.route('/mark-as-read', methods=['POST'])
def mark_notifications_as_unread():
    user_id = request.json.get('user_id')
    ret_val = NotificationService.mark_notification_as_read(user_id)
    return ret_val


@notification_routes.route('/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    NotificationService.delete_notification(notification_id)
    return jsonify({"message": "Notification deleted successfully"}), 200

@notification_routes.route('/user/<user_id>', methods=['GET'])
def get_user_notifications(user_id):
    notifications = NotificationService.get_user_notifications(user_id)
    if notifications:
        return notifications,200
    else:
        return {"message":"Error with getting notifications"},404
