import json
import os
class User:
    """User informations"""
    USERS_FILE = "users_data.json"
    user_counter = 1
    
    def __init__(self, name: str = None, phone_no: int = None, email: str = None) -> None:
        self._user_id = self.generate_user_id()
        self._name = name if name else 'SomeOne'
        self._phone_no = phone_no if phone_no else 0
        self._email = email if email else 'something@gmail.com'
        self.save_user_data()
        User.user_counter += 1

    def generate_user_id(self):
        try:
            with open('users_data.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []
            
        if not users:
            return 'USER-001'
        else:
            last_user = users[-1]
            last_id = last_user["user_id"]
            new_id_number = int(last_id.split('-')[1]) + 1
            new_user_id = f"USER-{new_id_number:03d}"
            return new_user_id
        
    @staticmethod
    def load_users_data():
        """Load users from the JSON file."""
        if os.path.exists(User.USERS_FILE):
            with open(User.USERS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_user_data(self):
        """Save the current user to the JSON file."""
        users = self.load_users_data()
        new_user = {
            'user_id': self._user_id,
            'name': self._name,
            'phone_no': self._phone_no,
            'email': self._email
        }
        users.append(new_user)
        
        with open(User.USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    
    def user_welcome(self):
        return f"Hi! {self._name} its a pleasure to see you using our website!"
    
    @property
    def user_id(self) -> str:
        """Getter Name"""
        return self._user_id

    @user_id.setter
    def name(self, value: str) -> None:
        """Setter Name"""
        self._user_id = value
        
    @property
    def name(self) -> str:
        """Getter Name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter Name"""
        self._name = value

    @property
    def phone_no(self) -> int:
        """Getter Phone Number"""
        return self._phone_no

    @phone_no.setter
    def phone_no(self, value: int) -> None:
        """Setter Phone Number"""
        self._phone_no = value

    @property
    def email(self) -> str:
        """Getter Email Address"""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Setter Email Address"""
        self._email = value
