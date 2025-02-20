from utils.jsonstorage import JSONStorage
from models.save_user_admin import SaveUserAdmin
from random import randint

class AdminUser:
    
    ADMIN_FILE = 'data/admins_data.json'
    admin_counter = 1
    def __init__(self,name,phone_no,email):
        self._name = name
        self._phone_no = phone_no
        self._email = email
        self._admin_id = self.generate_admin_id()
        self._password = self.generate_password()
        SaveUserAdmin.save_user_admin_data(self,'AdminType')
        AdminUser.admin_counter += 1
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        self._name = name
        
    @property
    def email(self):
        return self._email
    
    @property
    def phone_no(self):
        return self._phone_no
    
    @phone_no.setter
    def phone_no(self, phone_no):
        self._phone_no = phone_no
        
    @property
    def admin_id(self):
        return self._admin_id
    
    @property
    def password(self):
        return self._password
    
    def generate_admin_id(self):
        if (admins := JSONStorage.read_json_file(AdminUser.ADMIN_FILE)) is None:
            admins = []
        if not admins:
            return 'ADMIN-001'
        else:
            last_admin = admins[-1]
            last_id = last_admin["Admin Id"]
            new_id_number = int(last_id.split('-')[1]) + 1
            new_admin_id = f"ADMIN-{new_id_number:03d}"
            return new_admin_id
        
    def generate_password(self):
        return int(''.join(str(randint(0, 9)) for _ in range(5)))