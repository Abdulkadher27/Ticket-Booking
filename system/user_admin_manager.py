from models.user import User
from models.admin_user import AdminUser
import re

class UserAdminManager:

    @staticmethod
    def get_name():
        """Collect and validate user name."""
        while True:
            name = input("Enter Your Name: ").strip()
            if len(name) < 3 or len(name) > 30:
                print("The name should be between 3 and 30 characters.")
                continue
            if not all(char.isalpha() or char.isspace() for char in name):
                print("The name should only contain alphabets.")
                continue
            return name

    @staticmethod
    def get_phone():
        """Collect and validate phone number."""
        while True:        
            try:
                phone = int(input("Enter Your Phone Number: ").strip())
            except ValueError:
                print("The Phone Number should be Numbers")
            if len(str(phone)) != 10 or str(phone).startswith('0'):
                print("Invalid phone number! It should be 10 digits and not start with 0.")
                continue
            return phone

    @staticmethod
    def get_email():
        """Collect and validate email address."""
        while True:
            email = input("Enter Your Email Address: ").strip()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("Invalid email format!")
                continue
            return email

    @staticmethod
    def get_user_details(user_type):
        """Collect user details using separate functions for name, phone, and email."""
        name = UserAdminManager.get_name()
        phone = UserAdminManager.get_phone()
        email = UserAdminManager.get_email()
        
        if user_type == 'Admin':
            return AdminUser(name, phone, email)
        else:
            return User(name, phone, email)
