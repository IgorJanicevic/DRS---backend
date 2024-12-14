from repositories.friendship_repository import FriendshipRepository
from services.notification_service import NotificationService


class FriendshipService:

    @staticmethod
    def create_friendship(data):
        try:
            if FriendshipRepository.does_friendship_already_exist(data):
                return {'message': 'Friendship already exist'},403
            else:
                result= FriendshipRepository.create_friendship(data)
                NotificationService.create_notification_for_friendship(result)
                return result,201
        except:
            return {'message': 'Error with creating frienddship'},500
        
    @staticmethod
    def update_friendship(friendship_id,data):
        try:
            result = FriendshipRepository.update_friendship(friendship_id,data)
            if result:
                return {"message": "Friendship updated successfully", "data": result}, 200
            else:
                return {'message','Friendship not found'},404
        except:
            return {'message':'Error with updating friendship.'},500
        
    @staticmethod
    def get_all_friends_ids(user_id):
        try:
            result = FriendshipRepository.get_friends_ids(user_id)
            if result:
                return result
            else:
                return None
        except:
            return {'message': 'Error with getting friends'},500
        

    @staticmethod
    def get_friendship_status(user_id,friend_id):
        try:
            result = FriendshipRepository.does_friendship_already_exist({'user_id':user_id,'friend_id':friend_id})
            if result:
                if result['status'] == 'Accepted':
                    return 'Accepted'
                elif result['status'] == 'Pending':
                    if result['user_id'] == user_id:
                        return 'ISentRequest'
                    else:
                        return 'Pending'
            else:
                return 'None'
        except:
            return 'Error'

    
