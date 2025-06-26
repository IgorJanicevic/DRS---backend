from repositories.blocked_user_repository import BlockedUserRepository
from repositories.user_repository import UserRepository
from utils.email_utils import send_user_blocked_email


class BlockedUserService:

    @staticmethod
    def block_user_if_not_blocked(user_id):
        try:
            if BlockedUserRepository.is_user_blocked(user_id):
                print(f"User {user_id} is already blocked.")
                return False

            BlockedUserRepository.block_user(user_id)

            user = UserRepository.get_user_by_id(user_id)
            if user and user.get('email') and user.get('username'):
                try:
                    send_user_blocked_email(user['email'], user['username'])
                    print(f"Blocked user {user['username']} and sent email.")
                except Exception as e:
                    print(f"User blocked, but failed to send email: {e}")
            else:
                print(f"User with id {user_id} not found or missing email/username.")

            return True

        except Exception as e:
            print(f"Error in block_user_if_not_blocked: {e}")
            return False
        
    @staticmethod
    def is_user_blocked(user_id):
        try:
            return BlockedUserRepository.is_user_blocked(user_id)
        except Exception as e:
            print(f"Error checking if user {user_id} is blocked: {e}")
            return False
