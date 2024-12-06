from repositories.post_repository import PostRepository
from services.friendship_service import FriendshipService
from services.notification_service import NotificationService
from repositories.user_repository import UserRepository
from utils.email_utils import send_post_created_email, send_post_accepted_email,send_post_rejected_email
from config.config import Config
from app import send_post_to_admin
from datetime import datetime



class PostService:

    @staticmethod
    def create_post(data):
        post = PostRepository.create_post(data)
        if post:
            user= UserRepository.get_user_by_id(post['user_id'])
            #send_post_created_email(Config.ADMIN_EMAIL,post,user['username'])
            send_post_to_admin(post)
            
            
            
            return post,201
        else:
            return {'message': 'Error with create post.'},400
        
    @staticmethod
    def get_post_by_id(post_id):
        try:
            result = PostRepository.get_post_by_id(post_id)
            if result:
                return result,200
            else:
                return {"message": 'Post not found'},404
        except:
                return {"message": 'Error with getting post by id'},500
        
    @staticmethod
    def update_post(post_id,status,action=False):
        try:
            result= PostRepository.update_post(post_id,status)
            if result:
                user = UserRepository.get_user_by_id(result['user_id'])
                if action=='accept':
                    send_post_accepted_email(user['email'],result)
                elif action=='reject':
                    send_post_rejected_email(user['email'],result)
                    NotificationService.create_notification_for_rejected_post(post_id)
                    
                    # socketio.to(connected_users[str(user['_id'])]).emit('notification', {
                    #     'user_id': user['_id'],
                    #     'type': 'post_rejected',
                    #     'message': f"Objava sa ID {post_id} je odbijena",
                    #     'status': 'Rejected',
                    #     'created_at': datetime.utcnow().isoformat(), 
                    #     'metadata': {
                    #         'post_id': post_id,
                    #         'additional_info': 'Ova objava je odbijena iz razloga X'
                    #     }
                    # })
          
                    ##Zabeleziti za korisnika da mu je odbijena objava ++
                return result,200
            else:
                return {'message': 'Status cannot be chagned, post not found'},404
        except:
            return {'message':'Error with updating status'}  ,500
        
    @staticmethod
    def delete_post(post_id):
        try:
            if PostRepository.delete_post(post_id):
                return {'message':'Post successfully deleted.'},200
            else:
                return {'message': 'Post not found'},404
        except:
            return {'message': 'Error with deleting post'},500
        
    @staticmethod
    def get_user_posts(user_id):
        try:
            posts = PostRepository.get_user_posts(user_id)
            if posts:
                return posts,200
            else:
                return {'message': 'Posts not found'},404
        except:
            return {'message','Error with getting self posts'},500
        


    @staticmethod
    def get_pending_posts():
        try:
            posts = PostRepository.get_pending_posts()
            if posts:
                return posts,200
            else:
                return {'message':'Posts not found'},404
        except:
            return {'message','Error with getting posts'},500
            
    #Potrebno je da se ovo optimizuje da se ne pokupe svi postovi svih prijatelja vec npr 10 po 10, da se ne bi opteretilo sve
    #Zamsili da imas 700 prijatelja i da pokupis svaciji novi post
    #Potrebno je da se pokupe novi postovi
    @staticmethod
    def get_friends_posts(user_id):
        try:
            friends_ids= FriendshipService.get_all_friends_ids(user_id)
            posts= PostService.get_friend_newest_post(user_id)
            
            for friend_id in friends_ids:
                posts += PostService.get_friend_newest_post(friend_id)
                return posts,200
        except:
            return {'message':'Error with getting friends posts'},500
    
    @staticmethod
    def get_friend_newest_post(friend_id):
        posts= PostRepository.get_user_posts(friend_id)
        return posts

        