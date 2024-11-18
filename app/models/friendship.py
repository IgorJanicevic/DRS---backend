from datetime import datetime
class Friendship:
    def __init__(self,user_id,friend_id,timestamp=datetime.now()):
        self.user_id=user_id
        self.friend_id=friend_id
        self.timestamp=timestamp
        self.status= "Pending"

    def to_dict(self):
        return {
            "user_id":self.user_id,
            "friend_id":self.friend_id,
            "timestamp":self.timestamp,
            "status": self.status
        }
    

