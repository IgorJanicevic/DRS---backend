from flask_socketio import SocketIO

class SocketImplement:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.admin = None

    def set_socket(self, socketio: SocketIO):
        self.socketio = socketio

    def set_admin(self, admin: str):
        self.admin = admin

    def send_new_post(self, post: dict):
        if self.admin:
            self.socketio.emit('new_post', post, room=self.admin)
            print(f'Post successfully sent to admin {self.admin}')
        else:
            print('Admin is not set.')

    def send_notification(self, notification: dict, socket_id: str):
        self.socketio.emit('notification', notification, room=socket_id)
        print(f'Notification successfully sent to user {socket_id}')


socket_instance = None