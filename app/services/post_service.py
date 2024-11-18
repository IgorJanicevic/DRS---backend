from repositories.post_repository import PostRepository
from services.friendship_service import FriendshipService
from repositories.user_repository import UserRepository
from utils.email_utils import send_post_created_email, send_post_accepted_email,send_post_rejected_email
from config.config import Config



class PostService:

    @staticmethod
    def create_post(data):
        post = PostRepository.create_post(data)
        if post:
            user= UserRepository.get_user_by_id(post['user_id'])
            send_post_created_email(Config.ADMIN_EMAIL,post,user['username'])
            ##posalji adminu na pregled
            return post,201
        else:
            return {'message': 'Error with create post.'},400
        
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
                    ##Poslati korisniku na ispravku, bilo bi fino da i ovde bude soket
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
        


    #Potrebno je da se ovo optimizuje da se ne pokupe svi postovi svih prijatelja vec npr 10 po 10, da se ne bi opteretilo sve
    #Zamsili da imas 700 prijatelja i da pokupis svaciji novi post
    #Potrebno je da se pokupe novi postovi
    @staticmethod
    def get_friends_posts(user_id):
        try:
            friends_ids= FriendshipService.get_all_friends_ids(user_id)
            posts=[]
            for friend_id in friends_ids:
                posts += PostService.get_friend_newest_post(friend_id)
                return {'data':posts},200
        except:
            return {'message':'Error with getting friends posts'},500
    
    #TODOs
    @staticmethod
    def get_friend_newest_post(friend_id):
        return

        