from flask import Flask
from flask_pymongo import PyMongo
from config.config import Config
from flask_mail import Mail
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
mongo = PyMongo(app)  # Povezuje se sa MongoDB korišćenjem MONGO_URI
mail = Mail(app)      # Inicijalizacija Flask-Mail

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
    app.run(debug=True)


