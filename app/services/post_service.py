from repositories.post_repository import PostRepository
from services.friendship_service import FriendshipService
from services.notification_service import NotificationService
from repositories.user_repository import UserRepository
from services.blocked_user_service import BlockedUserService
from utils.email_utils import send_post_created_email, send_post_accepted_email,send_post_rejected_email
from extensions import socketio



class PostService:

    @staticmethod
    def create_post(data):
        user= UserRepository.get_user_by_id(data['user_id'])
        data['username'] = user['username']
        post = PostRepository.create_post(data)
        if post:
            # send_post_created_email(Config.ADMIN_EMAIL,post,user['username'])

            post['timestamp'] = post['timestamp'].isoformat()
            socketio.emit('new_post', post)
            print(f'Post successfully sent to admin') 
            
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
    def update_post(post_id,data,action=False):
        try:
            result= PostRepository.update_post(post_id,data)
            if result:
                user = UserRepository.get_user_by_id(result['user_id'])
                if action=='accept':
                    send_post_accepted_email(user['email'],result)
                elif action=='reject':
                    print(f"Sending rejection email..")
                    send_post_rejected_email(user['email'], result)
                    NotificationService.create_notification_for_rejected_post(post_id)

                    count = PostRepository.get_rejected_posts_count_by_user(user['_id'])
                    if count >= 3:
                        BlockedUserService.block_user_if_not_blocked(user['_id'])


                    
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
            
    #Pagination need to be done
    @staticmethod
    def get_friends_posts(user_id):
        try:
            friends_ids= FriendshipService.get_all_friends_ids(user_id)
            print('friends_ids:',friends_ids)

            posts= PostService.get_friend_newest_post(user_id)
            
            if posts == None and friends_ids ==None:
                return {'message':'Not found posts'},404
            elif posts != None and friends_ids == None:
                return posts,200
            
            for friend_id in friends_ids:
                posts += PostService.get_friend_newest_post(friend_id)
                return posts,200
        except:
            return {'message':'Error with getting friends posts'},500
    
    @staticmethod
    def get_friend_newest_post(friend_id):
        posts= PostRepository.get_user_posts(friend_id)
        return posts

        