from flask import Flask,request
from flask_pymongo import PyMongo
from config.config import Config
from flask_mail import Mail
from flask_cors import CORS
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
mongo = PyMongo(app)  # Povezuje se sa MongoDB korišćenjem MONGO_URI
mail = Mail(app)      # Inicijalizacija Flask-Mail
socketio = SocketIO(app,cors_allowed_origins="*")

# Pretpostavlja se da koristite neki oblik sesije ili baze podataka za čuvanje povezivanja
connected_users = {}

@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')  # Dohvatamo user_id iz query parametara
    if user_id:
        connected_users[str(user_id)] = request.sid  # Povezujemo user_id sa socket ID-jem
        print(f"User {user_id} connected with socket ID {request.sid}")
    else:
        print("User ID not provided")

@socketio.on('disconnect')
def handle_disconnect():
    for user_id, socket_id in connected_users.items():
        if socket_id == request.sid:
            del connected_users[user_id]
            print(f"User {user_id} disconnected")
            break




def create_app():
    from controllers.user_controller import user_routes
    from controllers.post_controller import post_routes
    from controllers.friendship_controller import friendship_routes
    from controllers.notifications_controller import notification_routes
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(post_routes,url_prefix='/post')
    app.register_blueprint(friendship_routes,url_prefix='/friendship')
    app.register_blueprint(notification_routes,url_prefix='/notification')
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app,debug=True,port=5000)


