from flask_mail import Message
from app import mail
from utils.jwttoken import generate_reset_token

def send_post_created_email(email, post, username):
    try:
        subject = f"New Post Created by {username}!"
        html_body = f"""
        <html>
            <body style=\"font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;\">
                <div style=\"max-width: 600px; margin: auto; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);\">
                    <div style=\"background-color: #4f46e5; color: white; padding: 20px; text-align: center;\">
                        <h2>New Post Created</h2>
                    </div>
                    <div style=\"padding: 20px; color: #333;\">
                        <p>User <strong>{username}</strong> has created a new post.</p>
                        <ul>
                            <li><strong>Description:</strong> {post.get('description', 'No description')}</li>
                            <li><strong>Created At:</strong> {post.get('timestamp', 'Unknown time')}</li>
                            <li><strong>Status:</strong> {post.get('status', 'Unknown status')}</li>
                        </ul>
                        <p>Please review it at your earliest convenience.</p>
                    </div>
                    <div style=\"background: #f1f5f9; text-align: center; padding: 12px; font-size: 13px; color: #777;\">
                        <p>Best regards, <br/> The DSMT Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        msg = Message(subject=subject,
                      sender="igorjanicevic33@gmail.com",
                      recipients=[email])
        msg.html = html_body
        mail.send(msg)
        return {"message": "Email sent successfully to administrator!"}, 200
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}, 500

def send_post_accepted_email(user_email, post):
    try:
        subject = "Your Post Has Been Accepted!"
        html_body = f"""
        <html>
            <body style=\"font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;\">
                <div style=\"max-width: 600px; margin: auto; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);\">
                    <div style=\"background-color: #16a34a; color: white; padding: 20px; text-align: center;\">
                        <h2>Post Accepted</h2>
                    </div>
                    <div style=\"padding: 20px; color: #333;\">
                        <p>Good news! Your post has been accepted.</p>
                        <ul>
                            <li><strong>Description:</strong> {post.get('description', 'No description')}</li>
                            <li><strong>Created At:</strong> {post.get('timestamp', 'Unknown time')}</li>
                            <li><strong>Status:</strong> {post.get('status', 'Accepted')}</li>
                        </ul>
                        <p>Thank you for contributing!</p>
                    </div>
                    <div style=\"background: #f1f5f9; text-align: center; padding: 12px; font-size: 13px; color: #777;\">
                        <p>Best regards, <br/> The DSMT Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        msg = Message(subject=subject,
                      sender="igorjanicevic33@gmail.com",
                      recipients=[user_email])
        msg.html = html_body
        mail.send(msg)
        return {"message": "Post accepted email sent successfully!"}, 200
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}, 500

def send_post_rejected_email(user_email, post):
    try:
        subject = "Your Post Has Been Rejected"
        html_body = f"""
        <html>
            <body style=\"font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;\">
                <div style=\"max-width: 600px; margin: auto; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);\">
                    <div style=\"background-color: #dc2626; color: white; padding: 20px; text-align: center;\">
                        <h2>Post Rejected</h2>
                    </div>
                    <div style=\"padding: 20px; color: #333;\">
                        <p>Unfortunately, your post has been rejected.</p>
                        <ul>
                            <li><strong>Description:</strong> {post.get('description', 'No description')}</li>
                            <li><strong>Created At:</strong> {post.get('timestamp', 'Unknown time')}</li>
                            <li><strong>Status:</strong> {post.get('status', 'Rejected')}</li>
                        </ul>
                        <p>If you have any questions, feel free to reach out to our support team.</p>
                    </div>
                    <div style=\"background: #f1f5f9; text-align: center; padding: 12px; font-size: 13px; color: #777;\">
                        <p>Best regards, <br/> The DSMT Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        msg = Message(subject=subject,
                      sender="igorjanicevic33@gmail.com",
                      recipients=[user_email])
        msg.html = html_body
        mail.send(msg)
        return {"message": "Post rejected email sent successfully!"}, 200
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}, 500
    try:
        subject = "Your Post Has Been Rejected"
        body = f"""
        Hi there,

        Unfortunately, your post has been rejected. Here are the details:
        
        - Description: {post.get('description', 'No description')}
        - Created At: {post.get('timestamp', 'Unknown time')}
        - Status: {post.get('status', 'Rejected')}
        
        If you have any questions, feel free to reach out.

        Best regards,
        The Team
        """
        msg = Message(subject=subject,
                      sender="igorjanicevic33@gmail.com", 
                      recipients=[user_email],
                      body=body)

        mail.send(msg)
        return {"message": "Post rejected email sent successfully!"}, 200
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}, 500

def send_registration_email(user_email, username,password):
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
                    <p>Your initial password is: {password}</p>
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
    mail.send(msg)

def send_reset_email(user):
    token = generate_reset_token(user)
    reset_url = f'http://localhost:5000/reset_password/{token}'
    
    msg = Message('Password Reset Request',
                  sender='igorjanicevic33@gmail.com',
                  recipients=[user.email])
    msg.body = f'Please visit the following link to reset your password: {reset_url}'
    
    mail.send(msg)

def send_user_blocked_email(user_email, username):
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
                    background-color: #dc2626;
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
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>Account Blocked Notification</h2>
                </div>
                <div class="content">
                    <p>Dear {username},</p>
                    <p>We regret to inform you that your account has been <strong>temporarily blocked</strong> due to multiple post rejections.</p>
                    <p>If you believe this was a mistake or wish to appeal, please contact our support team.</p>
                </div>
                <div class="footer">
                    <p>Best regards,<br>The DSMT Team</p>
                    <p>If you did not perform these actions, please contact us immediately.</p>
                </div>
            </div>
        </body>
    </html>
    """

    msg = Message('Your Account Has Been Blocked',
                  sender='igorjanicevic33@gmail.com',
                  recipients=[user_email])
    msg.html = html_body
    mail.send(msg)
