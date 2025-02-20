from abc import ABC, abstractmethod
from models.user import User
from typing import List

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float, seat_numbers: List[int],user: User) -> bool:
        """Process the payment for the given amount and seats."""
        pass
    
class PaymentProcessBluePrint(ABC):
    @abstractmethod
    def password_check() -> int:
        """Password Checking for each Process"""
        pass
    
    @abstractmethod
    def otp_generator(user: User) -> bool:
        """Generate OTP for each Transaction"""