class Post:
    def __init__(self,user_id,description,timestamp,type,status='Pending',image_url=None):
        self.user_id= user_id
        self.image_url= image_url
        self.description= description
        self.timestamp= timestamp
        self.type=type
        self.status= status

    def to_dict(self):
        return{
            "user_id":self.user_id,
            "image_url":self.image_url,
            "description":self.description,
            "timestamp":self.timestamp,
            "type":self.type,
            "status":self.status
        }