from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_session import Session
from flask_socketio import SocketIO
import os

mongo = PyMongo()
mail = Mail()
session = Session()

redis_url = os.getenv("REDIS_URL", "redis://default:6f0tJ3hSpWdpvhusFC6haVDYBqTgvtEE@redis-17861.c245.us-east-1-3.ec2.redns.redis-cloud.com:17861")

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    message_queue=redis_url
)
