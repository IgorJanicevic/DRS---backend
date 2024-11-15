from app import mongo
from bson.objectid import ObjectId  

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_user_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})
    
    @staticmethod
    def get_all_users():
        users = mongo.db.users.find()
        user_list = []

        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        return user_list

    @staticmethod
    def create_user(data):
        user = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "username": data['username'],
            "email": data['email'],
            "password": data['password'],
            "mobile": data['mobile'],
            "address": data['address'],
            "city": data['city'],
            "country": data['country'],
            "role": 'common',
            "first_login": True
        }
        
        result = mongo.db.users.insert_one(user)
        user['_id'] = str(result.inserted_id)  # Konvertovanje ID-a u string za lakoću rada
        return user

    @staticmethod
    def update_user(user_id, data):
        # Pronađi korisnika po ID-u
        user = UserRepository.get_user_by_id(user_id)
        
        if not user:
            return None  # Korisnik ne postoji

        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},  
            {"$set": data}
        )

        if result.modified_count > 0:
            updated_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            updated_user['_id'] = str(updated_user['_id'])  # Pretvori ObjectId u string
            return updated_user
        else:
            user['_id'] = str(user['_id'])  # Pretvori ObjectId u string
            return user

    
    @staticmethod
    def first_login_completed(user_id):
        user = UserRepository.get_user_by_id(user_id)
        
        if not user:
            return None
        
        user['first_login'] = False
        
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"first_login": False}}  
        )
        return mongo.db.users.find_one({"_id": ObjectId(user_id)}) if result.modified_count > 0 else None


    @staticmethod
    def delete_user(user_id):
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
