from models.bus import Bus
from system.bus_manager import BusManager
from models.booking_system import BookingSystem
from system.user_admin_manager import UserAdminManager
from utils.jsonstorage import JSONStorage
from abc import ABC, abstractmethod

class BookingManagerBlueprint(ABC):
    
    @classmethod
    @abstractmethod
    def change_num_seats(cls, total_seats: int) -> None:
        pass
    
    @classmethod
    @abstractmethod
    def change_seat_amount(cls,amount: int) -> None:
        pass
    
    @abstractmethod
    def book_ticket(self) -> None:
        pass
    
    @abstractmethod
    def cancel_ticket(self) -> None:
        pass
    
class BookingManager(BookingManagerBlueprint):
    
    BOOKING_FILE = 'data/booking_info.json'
    file = JSONStorage.read_json_file(BOOKING_FILE)
    total_seat = file['Total Seats']
    amount = file['Amount']
    
    @staticmethod
    def change_num_seats(total_seats: int) -> None:
        data = JSONStorage.read_json_file(BookingManager.BOOKING_FILE)
        data['Total Seats'] = total_seats
        JSONStorage.save_json(BookingManager.BOOKING_FILE,data)
        
    @staticmethod
    def change_seat_amount(amount: int) -> None:
        data = JSONStorage.read_json_file(BookingManager.BOOKING_FILE)
        data['Amount'] = amount
        JSONStorage.save_json(BookingManager.BOOKING_FILE,data)
        
    def __init__(self):
        self.booking_system = BookingSystem()

    def book_ticket(self):
        """Handle the booking process"""
        user = UserAdminManager.get_user_details('User')
        print(f"Hi!! {user.name}, Happy for choosing our website for Booking....\nHave a nice Journy!")
        available_buses = BusManager.display_available_buses()
        while True:
            bus_id = input("Enter the Bus ID to book: ")
            if bus_id not in available_buses.values():
                print("Enter the Valid BUS Id!")
                continue
            break
        selected_bus = next(({'Destination': city,'Bus Id': bus} for city, bus in available_buses.items() if bus == bus_id), None)

        if selected_bus:
            print(f"Booking seat on bus {bus_id} to {selected_bus['Destination']}...")
            bus = Bus(bus_id= bus_id, total_seats= BookingManager.total_seat)  
            seats = bus.get_seating_arrangement()
            while True:
                for seat in seats:
                    print(seat)
                print(f"Currently {len(bus.available_seats)} Number of seats available for this bus {bus.bus_id} to the {bus.destination}")
                num_seats = int(input(f"Enter Number of Seats {user.name} want to Book!"))
                if num_seats < 1 or num_seats > bus.available_number_seats:
                    print("Enter the valid number of seats")
                    continue
                break
            number_seats = []
            for _ in range(num_seats):
                for seat in seats:
                    print(seat)
                while True:    
                    seat_number = int(input("Enter the seat number to book: "))
                    if seat_number not in bus.available_seats:
                        print("Seat is already booked. Please choose another seat.")
                        continue
                    number_seats.append(seat_number)
                    break
            amount_per_seats = BookingManager.amount * num_seats    
            if self.booking_system.book_seat(bus, selected_bus['Destination'], user,num_seats,number_seats, amount_per_seats):
                print(f"Seat {', '.join(map(str, number_seats))} successfully booked for {user.name} on Bus {bus_id} to {selected_bus['Destination']}.")
        else:
            print("Invalid Bus ID! Please try again.")

    def cancel_ticket(self):
        """Handle the cancellation process"""
        user_id = input("Enter Your User ID: ")

        bookings = self.booking_system.load_booking_data()

        user_bookings = []
        for booking in bookings:
            if booking['User Id'] == user_id:
                user_bookings.append(booking)

        if not user_bookings:
            print("No bookings found for this user.")
            return

        print("Your bookings:")
        for i, booking in enumerate(user_bookings, start=1):
            print(f"{i}. Bus ID: {booking['Bus Id']} - Destination: {booking['Destination']}, Seats: {", ".join(map(str, booking['Seat Numbers']))}, Number of Seats: {booking['Number of Seats']}")

        bus_id_choice = input("Enter the Bus ID to cancel seats from (or 'cancel' to go back): ").strip()

        if bus_id_choice.lower() == 'cancel':
            print("Cancellation process aborted.")
            return

        selected_bookings = [booking for booking in user_bookings if booking['Bus Id'] == bus_id_choice]

        if not selected_bookings:
            print(f"No bookings found for Bus ID {bus_id_choice}.")
            return
        booked_seats = []
        print(f"Bookings found for Bus ID {bus_id_choice}:")
        for i, booking in enumerate(selected_bookings, start=1):
            print(f"{i}. Seats: {', '.join(map(str, booking['Seat Numbers']))} - Number of Seats: {booking['Number of Seats']}")
            booked_seats = booking['Seat Numbers']
         
        booking_choice = int(input("Enter the Number of Booking needs to cancel: "))
        if booking_choice < 1 or booking_choice > len(booked_seats):
            print("Invalid choice.")
            return
        
        selected_booking = []
        for _ in range(booking_choice):
            seat_number = int(input("Enter the seat number to cancel: "))
            selected_booking.append(seat_number)
        
        for seat in selected_booking:
            if seat not in booked_seats:
                print(f"Seat {seat} is not booked in your selected bus. Cancellation failed.")
                return

        bus = Bus(bus_id=bus_id_choice, total_seats=BookingManager.total_seat)  
        if self.booking_system.cancel_seat(bus, selected_booking):
            print(f"Seat {', '.join(map(str, selected_booking))} successfully cancelled for user {user_id} on Bus {bus_id_choice}.")
        else:
            print("Error in canceling the seat.")
