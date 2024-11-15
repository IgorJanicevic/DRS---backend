from repositories.user_repository import UserRepository
from utils.email_utils import send_registration_email, send_first_login_email
from werkzeug.security import generate_password_hash,check_password_hash
from utils.jwttoken import generate_token,verify_token
from config.config import Config
from flask import request
import requests

class UserService:
    
    @staticmethod
    def register_user(data):
        if UserRepository.get_user_by_username(data['username']):
            return {"message": "Username already exists."},400
        if UserRepository.get_user_by_email(data['email']):
            return {"message": "Email already exists."},400
        
        data['password'] = generate_password_hash(data['password'])
        user = UserRepository.create_user(data)
        print("OKEJ: " + user['email'])
        print("RADI: " + user['username'])
        send_registration_email(user['email'],user['username'])



        token = generate_token(user['_id'],user['role'])
        return {'token': token}, 200 
    
    @staticmethod
    def login_user(data):
        user = UserRepository.get_user_by_username(data['username'])
        if not user:
            return {'message':"Invalid credentials."},401
        
        try:
            password_correct = check_password_hash(user['password'], data['password'])
            if not user or not password_correct:
                return {'message': "Invalid credentials."},401        

            if user['first_login']:
                admin_email= Config.ADMIN_EMAIL
                send_first_login_email(admin_email,user['username'])
                user['first_login']=False

                UserRepository.first_login_completed(user['_id'])
                
                print("Successfully logged in")
            
        except Exception as e:
            return {"message": "Error with loggin in."}, 500
        
        token = generate_token(user['_id'],user['role']) 
        return {'token': token}, 200 
    
    
    def update_profile(user_id, data):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Authorization token is missing."}, 401

        try:
            decoded_token = verify_token(token)
            token_user_id = decoded_token['sub']

            if str(user_id) != str(token_user_id):
                return {"message": "Unauthorized access."}, 403

        except Exception as e:
            return {"message": f"Invalid or expired token: {str(e)}"}, 401

        updated_user = UserRepository.update_user(user_id, data)

        if updated_user:
            return updated_user, 200
        else:
            return {"message": "Failed to update user profile."}, 500
        

    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()
    
    
