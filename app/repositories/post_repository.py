from app import mongo
from bson.objectid import ObjectId
from datetime import datetime

class PostRepository:
    @staticmethod
    def get_post_by_id(post_id):
        return PostRepository.id_to_string(mongo.db.posts.find_one({"_id": ObjectId(post_id)}))
    
    @staticmethod
    def create_post(data):
        post_data = {
            "user_id": data['user_id'],
            "username": data['username'],
            "description": data['description'],
            "timestamp": datetime.now(),
            "type": data['type'],
            "status": "Pending",
            "image_url": data['image_url']
        }

        return PostRepository.id_to_string(post_data,mongo.db.posts.insert_one(post_data))
        

    @staticmethod
    def get_user_posts(user_id):
        posts_cursor = mongo.db.posts.find({"user_id": str(user_id),  "status":'Accepted'}).sort('timestamp',-1)
        posts = []
        for post in posts_cursor:
            if post['user_id']==user_id:
                post['_id'] = str(post['_id'])
                posts.append(post)
        return posts
    
    @staticmethod
    def get_pending_posts():
        posts_cursor = mongo.db.posts.find({"status": "Pending"}).sort('timestamp', -1)
        posts = []
        for post in posts_cursor:
            post['_id'] = str(post['_id'])
            if 'timestamp' in post and isinstance(post['timestamp'], datetime):
                post['timestamp'] = post['timestamp'].isoformat()
            posts.append(post)

        return posts

    

    @staticmethod
    def update_post(post_id,data):
        try:
            object_id = ObjectId(post_id)
            
            result = mongo.db.posts.update_one(
                {"_id": object_id}, 
                {"$set": data}       
            )
            
            if result.modified_count > 0:
                updated_post=mongo.db.posts.find_one({'_id':ObjectId(post_id)})
                updated_post['_id']= str(updated_post['_id'])
                return updated_post
            return False
        except Exception as e:
            print(f"Error updating post with ID {post_id}: {e}")
            return False    
    
    @staticmethod
    def delete_post(post_id):
        result = mongo.db.posts.delete_one({"_id":ObjectId(post_id)})
        return result.deleted_count > 0

    @staticmethod
    def id_to_string(data,result=False):
        if result:
            data['_id']= str(result.inserted_id)
        else:
            data['_id']= str(data['_id'])
        return data
    
    @staticmethod
    def get_rejected_posts_count_by_user(user_id):
        posts_cursor = mongo.db.posts.find({"user_id": str(user_id),  "status":'Rejected'})
        posts = []
        for post in posts_cursor:
            if post['user_id']==user_id:
                post['_id'] = str(post['_id'])
                posts.append(post)
        return len(posts)
