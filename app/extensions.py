from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_session import Session
from flask_socketio import SocketIO

mongo = PyMongo()
mail = Mail()
session = Session()
socketio = SocketIO(cors_allowed_origins="*")
