from utils.jsonstorage import JSONStorage
from system.bus_manager import BusManager
from abc import ABC, abstractmethod

class BusBueprint(ABC):
    @abstractmethod
    def get_seating_arrangement(self) -> list:
        pass

    @abstractmethod
    def book_seats(self, seat_numbers: list[int]) -> bool:
        pass

    @abstractmethod
    def cancel_seat(self, seat_number_list: list[int]) -> bool:
        pass

class Bus:
    
    booking_seats_json = 'data/booked_seats.json'
    
    def __init__(self, bus_id: str, total_seats: int) -> None:
        self._bus_id = bus_id
        self._total_seats = total_seats
        self._destination = BusManager.destination(bus_id)
        self.booked_seats = self.load_booked_seats()
        self.available_seats = set(range(1, total_seats + 1)) - self.booked_seats
        self.available_number_seats = len(self.available_seats)
        
    @property
    def bus_id(self) -> str:
        """Getter Bus Number"""
        return self._bus_id

    @bus_id.setter
    def bus_id(self, value: str) -> None:
        """Setter Bus Number"""
        self._bus_id = value
    
    @property
    def destination(self) -> str:
        """Getter for destination"""
        return self._destination
    
    @destination.setter
    def destination(self, value: str) -> None:
        """Setter for destination"""
        self._destination = BusManager.destination(value)
        
        
    def load_booked_seats(self):
        """Load the booked seats for the current bus from the JSON file."""
        if load_seats := JSONStorage.read_json_file(Bus.booking_seats_json):
            return set(load_seats.get(self.bus_id, []))  # Make sure it loads booked seats correctly
        else:
            return set() 
        
    def save_booked_seats(self):
        """Save the booked seats for the current bus to the JSON file."""
        data = JSONStorage.read_json_file(Bus.booking_seats_json)
        
        if data is None:
            data = {}  
        data[self.bus_id] = list(self.booked_seats)
        
        JSONStorage.save_json(Bus.booking_seats_json, data) 
            
    def book_seats(self, seat_numbers: list[int]) -> bool:
        """Book the requested seats if they are available."""
        self.booked_seats.update(seat_numbers)
        print(f"Seats {', '.join(map(str, seat_numbers))} have been successfully booked.")
        return True

    def cancel_seat(self, seat_number_list: list[int]) -> bool:
        """Cancel a booked seat."""
        for seat_number in seat_number_list:    
            if seat_number not in self.booked_seats:
                print(f"Seat {seat_number} is not booked yet!")
                return False
            else:
                self.booked_seats.remove(seat_number)
        self.save_booked_seats()
        return True

    def get_seating_arrangement(self) -> list:
        """Return the bus seat layout as a list of formatted rows."""
        cols = 4 
        rows = (self._total_seats + cols - 1) // cols  
        seating_layout = [] 

        for row in range(1, rows + 1):  
            seats_in_row = [(row - 1) * cols + i for i in range(1, cols + 1)]
            seat_display = [
                " B " if seat in self.booked_seats else f"{seat:2} "  
                for seat in seats_in_row
            ]
            seating_layout.append("|" + " ".join(seat_display) + "|")  

        return seating_layout

if __name__ == '__main__':
    pass