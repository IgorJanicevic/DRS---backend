class Notification:
    def __init__(self,user_id,type,message,status,created_at,metadata):
        self.user_id= user_id
        self.type= type # info,friend_request, post_rejcted
        self.message= message
        self.status= status # unread, read, deleted
        self.created_at= created_at
        self.metedate= metadata # id

    def to_dict(self):
        return{
            "user_id":self.user_id,
            "type":self.type,
            "message":self.message,
            "status":self.status,
            "created_at":self.created_at,
            "metadata":self.metedate
        }
    
    