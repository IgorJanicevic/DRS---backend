from app import mongo
from bson.objectid import ObjectId
from datetime import datetime
from models.friendship import Friendship

class FriendshipRepository:
    @staticmethod
    def create_friendship(data):
        ##friendship= Friendship(data['user_id'],data['friend_id'])   
        friendship = {
            'user_id':data['user_id'],
            'friend_id':data['friend_id'],
            'timestamp':datetime.now(),
            'status': 'Pending'
        }
        result= mongo.db.friendships.insert_one(friendship)
        friendship['_id']= str(result.inserted_id)
        return friendship
    
    @staticmethod
    def get_friendship_by_id(friendship_id):
        friendship = mongo.db.friendships.find_one({"_id":ObjectId(friendship_id)})
        friendship['_id'] = str(friendship['_id'])
        return friendship

    @staticmethod
    def does_friendship_already_exist(data):
        friendship = mongo.db.friendships.find_one({"user_id":data['user_id'],
                                                    "friend_id":data['friend_id']})
        return friendship
    #Potrebna je optimzacija
    @staticmethod
    def get_friends_ids(user_id):
        friends1= mongo.db.friendships.find({"user_id":user_id})
        friends2= mongo.db.friendships.find({"friend_id":user_id})
        friends_ids=[]
        if friends1:
            for friend in friends1:
                friends_ids.append(friend['friend_id'])
        if friends2:
            for friend in friends2:
                friends_ids.append(friend['user_id'])
        
        return friends_ids
    
    @staticmethod
    def update_friendship(friendship_id,data):
        friendship = FriendshipRepository.get_friendship_by_id(friendship_id)

        if not friendship:
            return None
        
        if '_id' in data:
            del data['_id']


        result = mongo.db.friendships.update_one(
            {"_id":ObjectId(friendship_id)},
            {"$set":data}
        )

        if result.modified_count > 0:
            return FriendshipRepository.get_friendship_by_id(friendship_id)
        else:
            return friendship
        
    @staticmethod
    def delete_friendship(friendship_id):
        result= mongo.db.friendships.delete_one({"_id":ObjectId(friendship_id)})
        return result.delete_count > 0
    