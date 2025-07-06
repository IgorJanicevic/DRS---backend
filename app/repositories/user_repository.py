from app import mongo
from bson.objectid import ObjectId  

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        user =mongo.db.users.find_one({"_id":ObjectId(user_id)})
        if user:
            user['_id']=str(user['_id'])
        return user

    @staticmethod
    def get_users_by_ids(user_objs):
        object_ids = [
            obj["user_id"] if isinstance(obj["user_id"], ObjectId) else ObjectId(obj["user_id"])
            for obj in user_objs
            if "user_id" in obj and ObjectId.is_valid(str(obj["user_id"]))
        ]

        users = mongo.db.users.find({"_id": {"$in": object_ids}})

        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            if 'password' in user:
                del user['password']
            user_list.append(user)

        return user_list


    @staticmethod
    def get_user_by_username(username):
        user = mongo.db.users.find_one({"username": username})
        if user:
            user['_id']=str(user['_id'])
        return user

    @staticmethod
    def get_user_by_email(email):
        user = mongo.db.users.find_one({"email": email})
        if user:
            user['_id']=str(user['_id'])        
        return user
    
    @staticmethod
    def get_all_users():
        users = mongo.db.users.find()
        user_list = []

        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        return user_list
    
    @staticmethod
    def get_searched_users(query):
        regex_default= {'$regex': f'^{query}', '$options': 'i'}
        terms = query.strip().split()
        and_conditions = []

        for term in terms:
            regex = {'$regex': f'^{term}', '$options': 'i'}
            and_conditions.append({
                '$or': [
                    {'username': regex_default},
                    {'email': regex_default},
                    {'first_name': regex},
                    {'last_name': regex},
                    {'city': regex_default},
                    {'country': regex_default},
                    {'address': regex_default},
                ]
            })

        users = mongo.db.users.find({'$and': and_conditions})

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
            "profile_img": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg",
            "first_login": True
        }
        
        result = mongo.db.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_user_by_id(user_id)
        
        if not user:
            return None

        if '_id' in data:
            del data['_id']

        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},  
            {"$set": data}
        )

        if result.modified_count > 0:
            updated_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            updated_user['_id'] = str(updated_user['_id']) 
            return updated_user
        else:
            user['_id'] = str(user['_id'])
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
    
    @staticmethod
    def id_to_string(user):
        user['_id']=str(user['_id'])
        return user
    
    from pymongo import MongoClient

    def search_users(query):
        users = UserRepository.get_searched_users(query)
            
        return users
    
    @staticmethod
    def get_users_by_city(city, limit, exclude_ids, user_id):
        query = {"city": city}

        if exclude_ids:
            query["_id"] = {"$nin": [ObjectId(id_) for id_ in exclude_ids]}

        if user_id:
            if "_id" in query:
                query["_id"]["$nin"].append(ObjectId(user_id))
            else:
                query["_id"] = {"$nin": [ObjectId(user_id)]}

        users = mongo.db.users.find(query).limit(limit)

        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        return user_list


    @staticmethod
    def get_random_users(limit):
        users = mongo.db.users.aggregate([
            {"$sample": {"size": limit}},
        ])

        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            if 'password' in user:
                del user['password']
            user_list.append(user)

        return user_list


