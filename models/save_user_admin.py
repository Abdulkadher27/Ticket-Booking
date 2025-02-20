from utils.jsonstorage import JSONStorage

class SaveUserAdmin:
    @staticmethod
    def load_users_admin_data(file):
        """Load users from the JSON file."""
        if load_data := JSONStorage.read_json_file(file):
            return load_data
        else:
            return []
        
    @staticmethod
    def is_admin_user(user_type):
        """Check if the user is an admin."""
        from models.user import User    
        from models.admin_user import AdminUser
        if user_type == 'AdminType':
            return AdminUser.ADMIN_FILE
        else:
            return User.USERS_FILE

    def save_user_admin_data(self,user_type):
        """Save the current user to the JSON file."""
        file = SaveUserAdmin.is_admin_user(user_type)
        users = SaveUserAdmin.load_users_admin_data(file)
        new_user = {}
        if user_type == 'AdminType':
            new_user['Admin Id'] = self.admin_id
        else:
            new_user['User Id'] = self.user_id
        new_user.update({
            'Name': self.name,
            'Phone Number': self.phone_no,
            'Email': self.email
        })
        if user_type == 'AdminType':
            new_user['Password'] = self.password
        users.append(new_user)
        JSONStorage.save_json(file,users)