import jwt
import datetime
from flask import current_app

def generate_token(user_id,role):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token važi 1 sat
    sub = str(user_id)
    payload = {
        'sub': sub,
        'exp': expiration_time,
        'role': role
    }
    
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    try:
        if token.startswith('Bearer '):
            token = token[7:]  # Skidamo 'Bearer ' (7 karaktera)
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload  # Return the user_id and role, exp too
    except jwt.ExpiredSignatureError:
        return None    # Token je istekao
    except jwt.InvalidTokenError:
        return None  # Nevažeći token
    

def generate_reset_token(user):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token važi 1 sat
    reset_token = jwt.encode({'reset_password': user.id, 'exp': expiration_time}, current_app.config['SECRET_KEY'], algorithm='HS256')
    return reset_token

