from system.user_admin_manager import UserAdminManager
from utils.jsonstorage import JSONStorage
from models.admin_user import AdminUser

class AdminManager:
    
    def create_admin_user(self):
        admin = UserAdminManager.get_user_details('Admin')
        print(f"Hello {admin.name}! Now you are in Admin Access!\nPlease remember the Password to login as an Admin {admin.password}")
        
    def enter_as_admin():
        admin_file = JSONStorage.read_json_file(AdminUser.ADMIN_FILE)
        admin_id = input("Enter Your Admin Access ID: ")
        admin_data = next((admin for admin in admin_file if admin["Admin Id"] == admin_id), None)
        if admin_data:
            for _ in range(3):
                try:
                    password = int(input("Enter The Password: "))
                except ValueError:
                    print("The Password Should be Numbers")
                    continue
                pass_word = admin_data['Password']
                if password == pass_word:
                    return True
                else:
                    print("Incorrect Password!")
            else:
                print("Sorry Too many incorrect passwords, Try again after sometimes!")
                return False
        else:
            print('No such a Admin Id')
            return False    
        
