from utils.jsonstorage import JSONStorage
from models.save_user_admin import SaveUserAdmin
from abc import ABC,abstractmethod

class UserBlueprint(ABC):
    
    @property
    @abstractmethod
    def user_id(self) -> str:
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def phone_no(self) -> int:
        pass

    @phone_no.setter
    @abstractmethod
    def phone_no(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @email.setter
    @abstractmethod
    def email(self, value: str) -> None:
        pass
    
class User(UserBlueprint):
    """User informations"""
    USERS_FILE = "data/users_data.json"
    user_counter = 1
    
    def __init__(self, name: str = None, phone_no: int = None, email: str = None) -> None:
        self._user_id = self.generate_user_id()
        self._name = name if name else 'SomeOne'
        self._phone_no = phone_no if phone_no else 0
        self._email = email if email else 'something@gmail.com'
        SaveUserAdmin.save_user_admin_data(self,'UserType')
        User.user_counter += 1

    def generate_user_id(self):
        if (users := JSONStorage.read_json_file(User.USERS_FILE)) is None:
            users = []
        if not users:
            return 'USER-001'
        else:
            last_user = users[-1]
            last_id = last_user["User Id"]
            new_id_number = int(last_id.split('-')[1]) + 1
            new_user_id = f"USER-{new_id_number:03d}"
            return new_user_id    
    
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
