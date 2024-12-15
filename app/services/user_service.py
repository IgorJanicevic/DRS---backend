from repositories.user_repository import UserRepository
from services.friendship_service import FriendshipService
from utils.email_utils import send_registration_email, send_first_login_email
from werkzeug.security import generate_password_hash,check_password_hash
from utils.jwttoken import generate_token,verify_token
from config.config import Config
from flask import request
import random,string,requests


class UserService:
    

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if(user):
            return user,200
        else:
            return {"message":"User not found"},404
        
    @staticmethod
    def get_suggested_friends(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if user:
            city = user['city']
            friends_ids = FriendshipService.get_all_friends_ids(user_id)
            five_suggested_users = UserService.get_five_suggested_users_by_city(city,friends_ids,user_id)
            return five_suggested_users,200
        else:
            return {'message': 'friends not found'}, 404
        
    @staticmethod
    def get_five_suggested_users_by_city(city, friends_ids,user_id):
        users = UserRepository.get_users_by_city(city, 5,friends_ids,user_id)
        if not users:
            users = UserRepository.get_random_users(limit=5)
        return users


            
    
    @staticmethod
    def register_user(data):
        if UserRepository.get_user_by_username(data['username']):
            return {"message": "Username already exists."},403
        if UserRepository.get_user_by_email(data['email']):
            return {"message": "Email already exists."},403
        
        new_password = UserService.generate_random_password()
        data['password'] = generate_password_hash(new_password)
        user = UserRepository.create_user(data)
        send_registration_email(user['email'],user['username'],new_password)



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
            return {"message": f"Invalid or expired token: {str(e)}"}, 500
        
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])

        updated_user = UserRepository.update_user(user_id, data)

        if updated_user:
            return updated_user, 200
        else:
            return {"message": "Failed to update user profile."}, 501
        

    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()
    
    @staticmethod
    def generate_random_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    
    @staticmethod
    def check_token(user_id):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Authorization token is missing."}, 401

        try:
            decoded_token = verify_token(token)
            token_user_id = decoded_token['sub']

            if str(user_id) != str(token_user_id):
                return {"message": "Unauthorized access."}, 403
            
            return True

        except Exception as e:
            return {"message": f"Invalid or expired token: {str(e)}"}, 401
        
    @staticmethod
    def search_users(query):
        if not query:
            return {"message": "Query parameter is missing"}, 400

        try:
            users = UserRepository.search_users(query)
            if not users:
                return {"message": "No users found."}, 404

            # Konverzija ObjectId u string
            for user in users:
                user['_id'] = str(user['_id'])
            
            return users, 200
        except Exception as e:
            return {"message": f"Error during search: {str(e)}"}, 500
