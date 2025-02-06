from models.user import User
from models.bus import Bus
from models.bus_manager import BusManager
from models.booking_system import BookingSystem

class BookingManager:
    def __init__(self):
        self.booking_system = BookingSystem()

    def get_user_details(self):
        """Collect and return user details"""
        name = input("Enter Your Name: ")
        phone = int(input("Enter Your Phone Number: "))
        email = input("Enter Your Email Address: ")
        user = User(email = email, phone_no = phone, name = name)
        print(user.user_welcome())
        return user
    
    def display_available_buses(self) -> dict[str]:
        """Display available buses"""
        bus_manager = BusManager()
        available_buses = bus_manager.show_available_buses()
        print("Available Buses:")
        for city, bus_id in available_buses.items():
            print(f"Bus ID: {bus_id} - Destination: {city}")
        return available_buses

    def book_ticket(self):
        """Handle the booking process"""
        user = self.get_user_details()
        available_buses = self.display_available_buses()
        bus_id = input("Enter the Bus ID to book: ")
        selected_bus = next(({'destination': city,'bus_id': bus} for city, bus in available_buses.items() if bus == bus_id), None)

        if selected_bus:
            print(f"Booking seat on bus {bus_id} to {selected_bus['destination']}...")
            bus = Bus(bus_id=bus_id, total_seats=48)  
            seats = bus.get_seating_arrangement()
            num_seats = int(input(f"Enter Number of Seats {user.name} want to Book!"))
            number_seats = []
            for _ in range(num_seats):
                for seat in seats:
                    print(seat)
                seat_number = int(input("Enter the seat number to book: "))
                number_seats.append(seat_number)
                
            if self.booking_system.book_seat(bus, selected_bus['destination'], user,num_seats,number_seats):
                print(f"Seat {number_seats} successfully booked for {user.name} on Bus {bus_id} to {selected_bus['destination']}.")
            else:
                print(f"Seat {seat_number} is already booked. Please choose another seat.")
        else:
            print("Invalid Bus ID! Please try again.")

    def cancel_ticket(self):
        """Handle the cancellation process"""
        user_id = input("Enter Your User ID: ")

        bookings = self.booking_system.load_booking_data()

        user_bookings = []
        for booking in bookings:
            if booking['user_id'] == user_id:
                user_bookings.append(booking)

        if not user_bookings:
            print("No bookings found for this user.")
            return

        print("Your bookings:")
        for i, booking in enumerate(user_bookings, start=1):
            # Correcting this line to display only seat numbers correctly
            print(f"{i}. Bus ID: {booking['bus_id']} - Destination: {booking['destination']}, Seats: {booking['seat_numbers']}, Number of Seats: {booking['num_seats']}")

        # Allow user to choose the bus_id to cancel from
        bus_id_choice = input("Enter the Bus ID to cancel seats from (or 'cancel' to go back): ").strip()

        if bus_id_choice.lower() == 'cancel':
            print("Cancellation process aborted.")
            return

        # Filter bookings by the chosen bus_id
        selected_bookings = [booking for booking in user_bookings if booking['bus_id'] == bus_id_choice]

        if not selected_bookings:
            print(f"No bookings found for Bus ID {bus_id_choice}.")
            return

        # Display available bookings for the chosen bus_id
        booked_seats = []
        print(f"Bookings found for Bus ID {bus_id_choice}:")
        for i, booking in enumerate(selected_bookings, start=1):
            # Correctly display seat numbers without showing the entire dictionary
            print(f"{i}. Seats: {', '.join(map(str, booking['seat_numbers']))} - Number of Seats: {booking['num_seats']}")
            booked_seats = booking['seat_numbers']
         
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

        # Create a bus object with the bus_id
        bus = Bus(bus_id=bus_id_choice, total_seats=48)  
        if self.booking_system.cancel_seat(bus, selected_booking):
            print(f"Seat {selected_booking} successfully cancelled for user {user_id} on Bus {bus_id_choice}.")
        else:
            print("Error in canceling the seat.")
