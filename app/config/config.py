import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://EuroHoopAdmin:stby9ZGGGqahFyZz@igorcluster.loyvk.mongodb.net/EuroHoopDb")

    SECRET_KEY = os.getenv("SECRET_KEY", "1a9b6e8c0f6d4f2a3b9d5e7c8a4f2b1d8c6f4e7d3a2f1c5b")

    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'igorjanicevic33@gmail.com'
    MAIL_PASSWORD = 'qamp lzyf pgxh ljro'
    ADMIN_EMAIL = "igorjanicevic33@gmail.com"

    SESSION_TYPE = 'filesystem'
