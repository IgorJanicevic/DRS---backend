from flask_mail import Message
from app import mail
from utils.jwttoken import generate_reset_token


def send_registration_email(user_email, username):
    html_body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f7fc;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                    font-size: 16px;
                    color: #333;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px;
                    background-color: #f4f7fc;
                    font-size: 12px;
                    color: #888;
                    border-radius: 0 0 8px 8px;
                }}
                .button {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin-top: 20px;
                }}
                .button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>Welcome to DSMT, {username}!</h2>
                </div>
                <div class="content">
                    <p>We're excited to have you on board. Your account has been successfully created!</p>
                    <p>If you have any questions or need help getting started, don't hesitate to reach out to us.</p>
                    <a href="https://dres.example.com" class="button">Get Started</a>
                </div>
                <div class="footer">
                    <p>Best regards, <br> The DSMT Team</p>
                    <p>If you did not register for this service, please disregard this email.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    msg = Message('Welcome to DRES',
                  sender='igorjanicevic33@gmail.com',
                  recipients=[user_email])
    msg.html = html_body  # Set the HTML content of the email
    mail.send(msg)

def send_first_login_email(administrator_email,username):
    html_body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f7fc;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                    font-size: 16px;
                    color: #333;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px;
                    background-color: #f4f7fc;
                    font-size: 12px;
                    color: #888;
                    border-radius: 0 0 8px 8px;
                }}
                .button {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin-top: 20px;
                }}
                .button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>Notification, {username} successfully logged in!!</h2>
                </div>
                <div class="content">
                    <p>Good job, our media is the best!</p>
                    <p>If you have any questions or need help getting started, don't hesitate to reach out to us.</p>
                    <a href="https://dres.example.com" class="button">Get Started</a>
                </div>
                <div class="footer">
                    <p>Best regards, <br> The DSMT Team</p>
                    <p>If you did not register for this service, please disregard this email.</p>
                </div>
            </div>
        </body>
    </html>
    """
    msg = Message('DRES Notification',
                  sender='igorjanicevic33@gmail.com',
                  recipients=[administrator_email])
    msg.html = html_body  # Set the HTML content of the email
    print("OVDE PROLAZ" + administrator_email)
    mail.send(msg)
    print("Sta je greska")

def send_reset_email(user):
    token = generate_reset_token(user)
    reset_url = f'http://localhost:5000/reset_password/{token}'
    
    msg = Message('Password Reset Request',
                  sender='igorjanicevic33@gmail.com',
                  recipients=[user.email])
    msg.body = f'Please visit the following link to reset your password: {reset_url}'
    
    mail.send(msg)

# def verify_reset_token(token):
#     try:
#         payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
#         return payload['reset_password']
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None

