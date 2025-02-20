import random

class OTPGenerator:
    @staticmethod
    def generate_otp(length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

