from app import mongo
from bson.objectid import ObjectId

class PostRepository:
    @staticmethod
    def get_post_by_id(post_id):
        return PostRepository.id_to_string(mongo.db.posts.find_one({"_id": ObjectId(post_id)}))
    
    @staticmethod
    def create_post(data):
        return PostRepository.id_to_string(mongo.db.posts.insert_one(data))
        

    @staticmethod
    def get_user_posts(user_id):
        posts = mongo.db.posts.find({"user_id":user_id})
        for post in posts:
            PostRepository.id_to_string(post)

        return posts
        
    @staticmethod
    def get_friends_posts(user_id):
        return
    
    @staticmethod
    def update_post(post_id,data):
        return
    
    @staticmethod
    def delete_post(post_id):
        result = mongo.db.posts.delete_one({"_id":ObjectId(post_id)})
        return result.deleted_count > 0

    @staticmethod
    def id_to_string(data):
        data['_id']= str(data['_id'])
        return data