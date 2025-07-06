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
    @staticmethod
    def get_all_blocked_users():
        try:
            userIds = BlockedUserRepository.get_all_blocked_users()
            users = UserRepository.get_users_by_ids(userIds)
            if not users:
                return {"status": 404, "message": "No blocked users found."}
            return {"status": 200, "data": users}
        except Exception as e:
            return {"status": 500, "message": f"Error fetching blocked users: {str(e)}"}

    @staticmethod
    def unblock_user(user_id):
        try:
            result = BlockedUserRepository.unblock_user(user_id)
            if result.deleted_count > 0:
                return {"status": 200, "message": f"User {user_id} unblocked successfully."}
            else:
                return {"status": 404, "message": f"User {user_id} not found in blocked list."}
        except Exception as e:
            return {"status": 500, "message": f"Error unblocking user: {str(e)}"}
