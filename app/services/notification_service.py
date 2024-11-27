# notification_service.py
from repositories.notification_repository import NotificationRepository
from repositories.user_repository import UserRepository
from repositories.post_repository import PostRepository

class NotificationService:
    @staticmethod
    def create_notification(notification):
        return NotificationRepository.create_notification(notification)

    @staticmethod
    def create_notification_for_friendship(friendship):
        user = UserRepository.get_user_by_id(friendship['user_id'])
        data = {"type":"friendship_request",
                "metadata":{"friendship_id":friendship['_id'],
                            "username":user['username'],
                            "friend_id":friendship['user_id']
                           },
                "message":"New friend request",
                "user_id":friendship['friend_id']}
        return NotificationRepository.create_notification(data)
    
    @staticmethod
    def create_notification_for_rejected_post(post_id):
        post = PostRepository.get_post_by_id(post_id)
        data = {
            "type":"post_rejected",
            "message":"Post has been rejected",
            "user_id":post['user_id'],
            "metadata":{
                "post_id":post_id
            }
        }
        return NotificationRepository.create_notification(data)
    

    @staticmethod
    def get_user_notifications(user_id):
        return NotificationRepository.get_notification_by_user(user_id)
    @staticmethod
    def mark_notification_as_read(user_id):
        return NotificationRepository.mark_as_read(user_id)
    
    @staticmethod
    def mark_notification_as_unread(user_id):
        return NotificationRepository.mark_as_read(user_id)
    
    @staticmethod
    def update_notification(notification_id,data):
        return NotificationRepository.update_notification(notification_id, data)

    @staticmethod
    def delete_notification(notification_id):
        return NotificationRepository.update_notification(notification_id,{"status":"deleted"})
    
