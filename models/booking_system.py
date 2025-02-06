from models.bus import Bus
from models.user import User
import json
import os

class BookingSystem:
    
    BOOKINGS_FILE = "bookings.json" 
    def __init__(self):
        self.booked_seats = self.load_booking_data()

    def cancel_seat(self, bus, seat_number : list[int]) -> bool:
        """
        Attempt to cancel a seat booking.
        If the seat is already booked, it will be released and reflect in the booking_seats.json file.
        """
        if bus.cancel_seat(seat_number):
            booked_seats = next((booking for booking in self.booked_seats if booking['bus_id'] == bus.bus_id), None)

            # Remove the seat from the booked seats
            for seats in seat_number:
                booked_seats['seat_numbers'].remove(seats)
                bus.available_seats.add(seats)
            
            # Save the updated booked seats to the booking_seats.json file
            self.save_cancelled_booking_data(bus.bus_id, booked_seats['seat_numbers'],len(seat_number))
            print(f"Seat {seat_number} has been successfully cancelled on bus {bus.bus_id}.")
            return True

    
    @staticmethod
    def load_booking_data():
        if os.path.exists(BookingSystem.BOOKINGS_FILE):
            with open(BookingSystem.BOOKINGS_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_booking_data(self,booking_info):
        bookings = self.load_booking_data()
        bookings.append(booking_info)
        with open(self.BOOKINGS_FILE, 'w') as f:
            json.dump(bookings, f, indent=4)
            
    def save_cancelled_booking_data(self,bus_id,booking_seats,count):
        bookings = self.load_booking_data()
        for booking in bookings: 
            if booking['bus_id'] == bus_id:
                booking['seat_numbers'] = booking_seats
                booking['num_seats'] -= count
                break

        with open(self.BOOKINGS_FILE, 'w') as f:
            json.dump(bookings, f, indent=4)
            
    def book_seat(self, bus: Bus, destination: str, user: User, num_seats: int, seat_numbers: list[int]) -> bool:
        if bus.book_seats(seat_numbers):
            booking_info = {
                "user_id": user.user_id,
                "name": user.name,
                "bus_id": bus.bus_id,
                "destination": destination,
                "num_seats": num_seats,
                "seat_numbers": seat_numbers
            }
            self.save_booking_data(booking_info)
            return True
        return False
