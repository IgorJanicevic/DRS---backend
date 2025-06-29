from app import mongo
from bson import ObjectId

class BlockedUserRepository:
    @staticmethod
    def block_user(user_id):
        return mongo.db.blockedUsers.insert_one({
            'user_id': ObjectId(user_id)
        })

    @staticmethod
    def is_user_blocked(user_id):
        return mongo.db.blockedUsers.find_one({'user_id': ObjectId(user_id)}) is not None
    
    @staticmethod
    def get_all_blocked_users():
        blocked = mongo.db.blockedUsers.find()
        return list(blocked)

    @staticmethod
    def unblock_user(user_id):
        return mongo.db.blockedUsers.delete_one({'user_id': ObjectId(user_id)})

