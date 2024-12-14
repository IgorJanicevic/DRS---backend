from datetime import datetime
from bson import ObjectId
from flask import Flask, request, jsonify
from flask_session import Session
from flask_pymongo import PyMongo
from config.config import Config
from flask_mail import Mail
from flask_cors import CORS
from flask_socketio import SocketIO,rooms
# from socket_implement import SocketImplement


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
app.secret_key = "some_secret_key"
Session(app)

mongo = PyMongo(app)
mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
# socket_implement = SocketImplement(socketio)

# Globalna promenljiva za admin socket
admin_socket_id = None

# Povezivanje admina na SocketIO
@socketio.on('connect')
def handle_connect():
    global admin_socket_id
    user_id = request.args.get('user_id')
    role = request.args.get('role')

    # Ako je korisnik admin, sačuvaj njegov socket_id
    if role == 'admin':
        admin_socket_id = request.sid
        print(f"Admin connected: {user_id} with socket_id: {admin_socket_id}")
        # socket_implement.set_admin(admin_socket_id)


# Kreiranje objave od strane korisnik
@app.route('/post/create', methods=['POST'])
def create_post():
    data = request.get_json()
    user =mongo.db.users.find_one({"_id":ObjectId(data['user_id'])})
    if user:
        user['_id']=str(user['_id'])
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

    ret_val = id_to_string(post_data,mongo.db.posts.insert_one(post_data))    
    if ret_val:
        socketio.emit('new_post', ret_val, room=admin_socket_id)
        return ret_val, 201
    else:    
        return jsonify({"message": "Error."}), 400


@staticmethod
def id_to_string(data,result=False):
    if result:
        data['_id']= str(result.inserted_id)
        data['timestamp']= str(data['timestamp'])
    else:
        data['_id']= str(data['_id'])

    return data

def create_app():
    from controllers.user_controller import user_routes
    from controllers.post_controller import post_routes
    from controllers.friendship_controller import friendship_routes
    from controllers.notifications_controller import notification_routes
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(post_routes, url_prefix='/post')
    app.register_blueprint(friendship_routes, url_prefix='/friendship')
    app.register_blueprint(notification_routes, url_prefix='/notification')
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, port=5000)