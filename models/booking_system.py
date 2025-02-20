from models.bus import Bus
from models.user import User
from utils.jsonstorage import JSONStorage
from payment.upi_payment import UPIPaymentMethod 
from payment.credit_card import CreditCardPaymentMethod
from payment.depit_card import DebitCardPaymentMethod
from abc import ABC, abstractmethod

class BookingSystemBlueprint(ABC):
    @abstractmethod
    def cancel_seat(self, bus, seat_number : list[int]) -> bool:
        pass
    
    @abstractmethod
    def load_booking_data(self) -> list[dict]:
        pass
    
    @abstractmethod
    def save_booking_data(self,booking_info) -> None:
        pass
    
    @abstractmethod
    def save_cancelled_booking_data(self,bus_id: str,booking_seats: list[int] ,count: int) -> None:
        pass
    
    @abstractmethod
    def book_seat(self, bus: Bus, destination: str, user: User, num_seats: int, seat_numbers: list[int]) -> bool:
        pass
    
class BookingSystem(BookingSystemBlueprint):
    
    BOOKINGS_FILE = "data/bookings.json" 
    def __init__(self) -> None:
        self.booked_seats = self.load_booking_data()

    def cancel_seat(self, bus: Bus, seat_number : list[int]) -> bool:
        """
        Attempt to cancel a seat booking.
        If the seat is already booked, it will be released and reflect in the booking_seats.json file.
        """
        if bus.cancel_seat(seat_number):
            booked_seats = next((booking for booking in self.booked_seats if booking['Bus Id'] == bus.bus_id), None)
            for seats in seat_number:
                booked_seats['Seat Numbers'].remove(seats)
                bus.available_seats.add(seats)
            self.save_cancelled_booking_data(bus.bus_id, booked_seats['Seat Numbers'],len(seat_number))
            return True

    
    @staticmethod
    def load_booking_data() -> list[dict]:
        if load_data := JSONStorage.read_json_file(BookingSystem.BOOKINGS_FILE):
            return load_data
        else:
            return []
    
    def save_booking_data(self,booking_info) -> None:
        bookings = self.load_booking_data()
        bookings.append(booking_info)
        JSONStorage.save_json(BookingSystem.BOOKINGS_FILE, bookings)
            
    def save_cancelled_booking_data(self,bus_id: str,booking_seats: list[int],count: int) -> None:
        bookings = self.load_booking_data()
        for booking in bookings: 
            amount = booking['Amount'] / booking['Number of Seats']
            if booking['Bus Id'] == bus_id:
                booking['Seat Numbers'] = booking_seats
                booking['Number of Seats'] -= count
                booking['Amount'] -= count * amount
                break
        JSONStorage.save_json(self.BOOKINGS_FILE,bookings)
            
    def book_seat(self, bus: Bus, destination: str, user: User, num_seats: int, seat_numbers: list[int], amount: float) -> bool:
        if bus.book_seats(seat_numbers):
            booking_info = {
                "User Id": user.user_id,
                "Name": user.name,
                "Bus Id": bus.bus_id,
                "Destination": destination,
                "Number of Seats": num_seats,
                "Seat Numbers": seat_numbers,
                "Amount": amount
            }
            choice = int(input(f"You have to pay {amount} and select the mode of Transcation\n1. Credit Card Payment\n2. Debit Card Payment\n3. UPI Payment\nEnter the Payment Method:  "))
            while True:
                match choice:
                    case 3:
                        upi = UPIPaymentMethod()
                        if upi.process_payment(amount,seat_numbers,user):
                            self.save_booking_data(booking_info)
                            bus.save_booked_seats()
                            break
                        else:
                            False
                    case 1:
                        credit = CreditCardPaymentMethod()
                        if credit.process_payment(amount, seat_numbers,user):
                            self.save_booking_data(booking_info)
                            bus.save_booked_seats()
                            break
                        else:
                            return False
                    case 2:
                        debit = DebitCardPaymentMethod()
                        if debit.process_payment(amount, seat_numbers,user):
                            self.save_booking_data(booking_info)
                            bus.save_booked_seats()
                            break
                        else:
                            return False
                    case _:
                        print("We only support UPI Card/Debit Card payment")
                    
            return True
        return False

if __name__ == '__main__':
    pass