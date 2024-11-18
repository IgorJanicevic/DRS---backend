class User:
    def __init__(self, first_name, last_name, address=None, city=None, country=None, mobile=None, 
                 email=None, username=None, password=None, role='common'):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.country = country
        self.mobile = mobile
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.first_login = True 
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "mobile": self.mobile,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "first_login": self.first_login
        }
