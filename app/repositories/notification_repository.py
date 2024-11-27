from datetime import datetime
from app import mongo
from bson import ObjectId
from models.notification import Notification


class NotificationRepository:

    @staticmethod
    def get_notification_by_id(noty_id):
        return NotificationRepository.id_to_string(mongo.db.notifications.find_one({"_id":ObjectId(noty_id)}))
    
    @staticmethod
    def create_notification(data):
        create = {
            'user_id': data['user_id'],
            'message': data['message'],
            'type': data.get('type', 'info'), 
            'status': data.get('status', 'unread'),
            'created_at': data.get('created_at', datetime.utcnow().isoformat()), 
            'metadata': data.get('metadata', {}) 
        }

        return NotificationRepository.id_to_string(data,mongo.db.notifications.insert_one(create))
    
    @staticmethod
    def get_notification_by_user(user_id):
        notifications = mongo.db.notifications.find({"user_id": user_id, "status": {"$ne": "deleted"}}).sort("created_at", -1)
        ret_val = []

        for noty in notifications:
            noty['_id'] = str(noty['_id'])
            ret_val.append(noty)

        return ret_val


    @staticmethod
    def update_notification(_id,data):
        try:
            result = mongo.db.notification.update_one(
                {"_id":ObjectId(_id)},
                {"$set":data}
            )

            if result.modified_count > 0:
                updated_notification = mongo.db.notifications.find_one({"_id":ObjectId(_id)})
                updated_notification['_id']  = str(updated_notification['_id'])
                return updated_notification
            else:
                return False
        except Exception as e:
            print(f'Error updating notification with')
            return False
        
    @staticmethod
    def mark_as_read(user_id):
        notifications = mongo.db.notifications.update_many(
            {"user_id": user_id, "status": "unread"},
            {"$set": {"status": "read"}}
        )
        if notifications.modified_count > 0:
            return {"message": "Notifications marked as unread"}, 200
        else:
            return {"message": "No notifications found to update"}, 404


    @staticmethod
    def id_to_string(data,result=False):
        if result:
            data['_id']= str(result.inserted_id)
        else:
            data['_id']= str(data['_id'])
        return data


