from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_session import Session
from flask_socketio import SocketIO
import os

mongo = PyMongo()
mail = Mail()
session = Session()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    message_queue=redis_url
)
