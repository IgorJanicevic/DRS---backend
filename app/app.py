from flask import Flask, request, session
from flask_session import Session
from flask_pymongo import PyMongo
from config.config import Config
from flask_mail import Mail
from flask_cors import CORS
from flask_socketio import SocketIO,rooms


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
app.secret_key = "some_secret_key"
Session(app)

mongo = PyMongo(app)
mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Globalna promenljiva za admin socket
connected_users = {}
session_collection = mongo.db.sessions


def send_post_to_admin(post):
    admin_session = session_collection.find_one({"role": "admin"})
    if admin_session:
        socketio.emit("new_post", post, to=admin_session["socket_id"])
        print("Poslato je adminu na pregled: ", admin_session["socket_id"])
    else:
        print("Nema povezanog admina za slanje posta.")


def notify_clients(message):
    client_sessions = session_collection.find({"role": {"$ne": "admin"}})
    for client in client_sessions:
        socketio.emit("notification", message, to=client["socket_id"])
        print(f"Poruka poslata klijentu sa id: {client['user_id']}")


@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    role = request.args.get('role')

    if user_id and role != 'admin':
        # Ažuriraj ili dodaj korisnika u bazu
        session_collection.update_one(
            {"user_id": user_id},
            {"$set": {"socket_id": request.sid, "role": role}},
            upsert=True
        )
        print(f"Korisnik sa id: {user_id} i rolom: {role} se uspesno povezao sa socket id: {request.sid}")
    
    elif role == 'admin':
        # Provera i ažuriranje za admina
        existing_admin = session_collection.find_one({"role": "admin"})
        if existing_admin:
            print(f"Admin je već povezan. Prekidam prethodnu sesiju sa socket id: {existing_admin['socket_id']}")
            # Ažuriraj socket_id za admina
            session_collection.update_one(
                {"role": "admin"},
                {"$set": {"socket_id": request.sid}},
                upsert=True
            )
        else:
            # Dodaj novog admina
            session_collection.update_one(
                {"role": "admin"},
                {"$set": {"socket_id": request.sid, "user_id": user_id}},
                upsert=True
            )
            print(f"Admin se uspesno povezao sa socket id: {request.sid} i id: {user_id}")
    else:
        print("Nisu pronađeni potrebni parametri za povezivanje.")

@socketio.on('disconnect')
def handle_disconnect():
    print('Korisnik se odvezao')

    # Obrisi sesiju iz baze
    disconnected_session = session_collection.find_one_and_delete({"socket_id": request.sid})

    if disconnected_session:
        print(f"Korisnik sa id: {disconnected_session.get('user_id')} i rolom: {disconnected_session.get('role')} se diskonektovao.")
    else:
        print("Sesija nije pronađena u bazi.")

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
