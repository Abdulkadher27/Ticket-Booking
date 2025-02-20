from payment.payment import PaymentMethod
from payment.paymentprocess import PaymentProcess
from models.user import User

class UPIPaymentMethod(PaymentMethod):
    def process_payment(self, amount: float, seat_numbers: list[int],user: User) -> bool:
        upi_id = PaymentProcess.id_check_upi()
        print(f"You have to pay {amount} for {", ".join(map(str, seat_numbers))} you have Booked!")
        choice = input("Press Yes to pay! ")
        if choice.lower() == 'yes':
            upi_pass = PaymentProcess.password_check()
            if PaymentProcess.otp_checker(user):
                print("Transaction Success!")
                return True
            else:
                return False
        else:
            return False    
            
            