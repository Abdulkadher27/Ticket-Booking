from utils.jsonstorage import JSONStorage

class BusManager:
    
    DESTINATION_FILE = "data/destinations.json"
    def __init__(self) -> None:
        self.destinations = self.load_destinations()
        self.buses = self.generate_buses()

    def load_destinations(self) -> list[str]:
        """Load destinations from a file."""
        data = JSONStorage.read_json_file(BusManager.DESTINATION_FILE)
        return data.get("Cities",[])

    def save_destinations(self,cities: list[str]) -> None:
        """Save destinations to a file."""
        JSONStorage.save_json(BusManager.DESTINATION_FILE, {"Cities": cities})

    def add_destination(self, new_destination: str) -> bool:
        """Add a new destination and save to file."""
        cities = self.load_destinations()
        
        if new_destination not in cities:
            cities.append(new_destination)
            self.save_destinations(cities) 
            self.buses = self.generate_buses()  
            return True
            
    @staticmethod
    def display_available_buses() -> dict[str]:
        """Display available buses"""
        bus_manager = BusManager()
        available_buses = bus_manager.show_available_buses()
        print("Available Buses:")
        for city, bus_id in available_buses.items():
            print(f"Bus ID: {bus_id} - Destination: {city}")
        return available_buses
    
    @staticmethod
    def destination(bus_id: str) -> str | None:
        bus_manager = BusManager()
        for destination, id in bus_manager.buses.items():
            if id == bus_id:
                return destination
        return None
    
    def generate_buses(self) -> dict[str, str]:
        """Create a dictionary of buses with unique codes."""
        return {destination: f"BUS-{str(i+1).zfill(3)}" for i, destination in enumerate(self.destinations)}
    
    def show_available_buses(self) -> dict[str, str]:
        """Return the available buses with unique codes."""
        return {city: self.buses[city] for city in self.buses}
