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
