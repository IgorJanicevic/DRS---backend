from flask import Flask
from flask_cors import CORS
from socket_handler import register_socket_events
from config.config import Config
from extensions import mongo, mail, session, socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicijalizuj ekstenzije
    mongo.init_app(app)
    mail.init_app(app)
    session.init_app(app)
    socketio.init_app(app)

    # Registruj socket eventove
    register_socket_events(socketio)

    # Registruj blueprintove
    from controllers.user_controller import user_routes
    from controllers.post_controller import post_routes
    from controllers.friendship_controller import friendship_routes
    from controllers.blocked_user_controller import blocked_user_routes
    from controllers.notifications_controller import notification_routes

    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(post_routes, url_prefix='/post')
    app.register_blueprint(friendship_routes, url_prefix='/friendship')
    app.register_blueprint(blocked_user_routes, url_prefix='/blocked')
    app.register_blueprint(notification_routes, url_prefix='/notification')

    CORS(app, origins=[
            "http://localhost:3000",
            "https://drs-frontend.vercel.app"
        ], supports_credentials=True)
    
    return app
