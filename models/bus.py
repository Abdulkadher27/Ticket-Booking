import json

class Bus:
    
    booking_seats_json = 'booked_seats.json'
    
    def __init__(self, bus_id: str, total_seats: int) -> None:
        self._bus_id = bus_id
        self._total_seats = total_seats
        self.booked_seats = self.load_booked_seats()
        self.available_seats = set(range(1, total_seats + 1)) - self.booked_seats
        
    @property
    def bus_id(self) -> str:
        """Getter Bus Number"""
        return self._bus_id

    @bus_id.setter
    def name(self, value: str) -> None:
        """Setter Bus Number"""
        self._bus_id = value
    
    def load_booked_seats(self):
        """Load the booked seats for the current bus from the JSON file."""
        try:
            with open(Bus.booking_seats_json, 'r') as file:
                data = json.load(file)
                return set(data.get(self.bus_id, []))  # Make sure it loads booked seats correctly
        except (FileNotFoundError, json.JSONDecodeError):
            return set()  # Return an empty set if the file is not found or is empty

        
    def save_booked_seats(self):
        """Save the booked seats for the current bus to the JSON file."""
        try:
            with open(Bus.booking_seats_json, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}  # If the file doesn't exist or is corrupted, start with an empty dictionary
            
        # Update the booked seats list for the current bus
        data[self.bus_id] = list(self.booked_seats)
        
        # Save the updated data back to the JSON file
        with open(Bus.booking_seats_json, 'w') as file:
            json.dump(data, file, indent=4)

            
    def is_seat_available(self, seat_numbers: list[int]) -> bool:
        """Check if the requested seats are available."""
        return not any(seat in self.booked_seats for seat in seat_numbers)

    def book_seats(self, seat_numbers: list[int]) -> bool:
        """Book the requested seats if they are available."""
        if not self.is_seat_available(seat_numbers):
            print(f"The following seats are already booked: {', '.join(map(str, seat_numbers))}. Please choose other seats.")
            return False
        
        # Update the booked seats
        self.booked_seats.update(seat_numbers)
        
        # Save the updated booking info
        self.save_booked_seats()
        
        print(f"Seats {', '.join(map(str, seat_numbers))} have been successfully booked.")
        return True

    def cancel_seat(self, seat_number_list: list[int]) -> bool:
        """Cancel a booked seat."""
        print(seat_number_list)
        for seat_number in seat_number_list:    
            if seat_number not in self.booked_seats:
                print(f"Seat {seat_number} is not booked yet!")
                return False
            else:
                self.booked_seats.remove(seat_number)
        
        # Save the updated booked seats after cancellation
        self.save_booked_seats()
        
        print(f"Seat {seat_number_list} has been successfully cancelled.")
        return True

    def get_seating_arrangement(self) -> list:
        """Return the bus seat layout as a list of formatted rows."""
        cols = 4  # Number of columns
        rows = (self._total_seats + cols - 1) // cols  # Calculate the number of rows, ensuring no rounding errors
        seating_layout = [] 

        for row in range(1, rows + 1):  
            # Create a list of seat numbers for each row
            seats_in_row = [(row - 1) * cols + i for i in range(1, cols + 1)]

            # Format each seat as " B " (booked) or "  1 " (available)
            seat_display = [
                " B " if seat in self.booked_seats else f"{seat:2} "  
                for seat in seats_in_row
            ]

            # Join the seats with spaces and wrap them in pipes
            seating_layout.append("|" + " ".join(seat_display) + "|")  

        return seating_layout
