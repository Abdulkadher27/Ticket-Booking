from payment.payment import PaymentMethod
from models.user import User
from payment.paymentprocess import PaymentProcess

class CreditCardPaymentMethod(PaymentMethod):
    
    def process_payment(self, amount: int, seat_numbers : list[int], user: User) -> bool:
        credit_id= PaymentProcess.id_check()
        print(f"You have to pay {amount} for seats {', '.join(map(str, seat_numbers))} you have booked!")
        choice = input("Press YES to pay! ")
        if choice.lower() == 'yes':
            credit_pass = PaymentProcess.password_check()
            if PaymentProcess.otp_checker(user):
                print("Transcation Succes!")
                return True
            else:
                return False
        else:
            return False
    
        