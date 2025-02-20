from payment.payment import PaymentMethod
from payment.paymentprocess import PaymentProcess
from models.user import User

class DebitCardPaymentMethod(PaymentMethod):
    def process_payment(self, amount: float, seat_numbers: list[int],user: User) -> bool:
        card_number = PaymentProcess.id_check()
        print(f"You have to pay {amount} for seats {', '.join(map(str, seat_numbers))} you have booked!")
        choice = input("Press YES to pay! ")
        if choice.lower() == 'yes':
            debit_pass = PaymentProcess.password_check()
            if PaymentProcess.otp_checker(user):
                print("Transaction Success!")
                return True
            else:
                return False
        else:
            return False    
        
        
        