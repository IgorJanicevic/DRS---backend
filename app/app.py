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
socketio = SocketIO(app,cors_allowed_origins="http://localhost:3000")

# Pretpostavlja se da koristite neki oblik sesije ili baze podataka za čuvanje povezivanja
connected_users = {}
admin_socket= None


def send_post_to_admin(post):
    global admin_socket
    socketio.emit("new_post", post)
   # print("Poslato je lepo",to=admin_socket)

@socketio.on('connect')
def handle_connect():
    global admin_socket

    user_id = request.args.get('user_id')  # Dohvat user_id iz query parametara
    role = request.args.get('role')        # Dohvat role iz query parametara

    if user_id and role != 'admin':
        connected_users[str(user_id)] = {
            "socket_id": request.sid,
            "role": role
        }
        print(f"Korisnik sa id: {user_id} i rolom: {role} se uspesno povezao sa socket id: {request.sid}")
    
    if role == 'admin':
        admin_socket = request.sid
        socketio.emit("connect", request.sid ,to=admin_socket)
        print(f"Admin se uspesno povezao sa socket id: {admin_socket} sa id: {user_id}")
    else:
        print(f"Nisu pronađeni potrebni parametri za povezivanje evo admin sokcet {admin_socket}.")

    print(admin_socket)


@socketio.on('disconnect')
def handle_disconnect():
    for user_id, socket_id in connected_users.items():
        if socket_id == request.sid:
            del connected_users[user_id]
            print(f"Korisnik sa id: {user_id} se diskonektovao")
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

