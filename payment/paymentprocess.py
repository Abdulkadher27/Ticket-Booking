from utils.otp_generator import OTPGenerator as OTP
from payment.payment import PaymentProcessBluePrint
from models.user import User
import re

class PaymentProcess(PaymentProcessBluePrint):
    @staticmethod
    def id_check() -> int:
        while True:
            try:
                id = int(input("Enter Your Credit/Debit Card ID: "))
            except ValueError:
                print("The Credit/Debit Cards should be Numbers")
                continue
            if len(str(id)) != 16 or str(id).startswith('0'):
                print("The Credit/Debit Card should contain 16 valid numbers!")
                continue
            break
        return id
    
    @staticmethod
    def id_check_upi():
        while True:
            id = input("Enter Your UPI ID: ")
            if not re.match(r'^[a-zA-Z]+@[a-zA-Z]+$', id):
                print("Invalid UPI ID")
                continue
            break
        return id
        
    @staticmethod
    def password_check():
        while True:
            try:
                password = int(input("Enter the Pin!"))
            except ValueError:
                print("The Passwords should be Numbers")
                continue
            if len(str(password)) < 3 or len(str(password)) > 6:
                print("Invalid Password")
                continue
            break
        return password
        
    @staticmethod
    def otp_checker(user: User) -> bool:
        for _ in range(3):
            otp = int(OTP.generate_otp())
            print(f"The OTP for this number {user.phone_no} is {otp}")
            otp_user = int(input(f"Enter the OTP send to this Phone number {user.phone_no}: "))
            if otp == otp_user:
                break
            else:
                print("Invalid OTP")
        else:
            return False
        return True