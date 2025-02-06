
class BusManager:
    def __init__(self) -> None:
        self.destinations = ["Chennai", "Bangalore", "Tenkasi", "Coimbatore", "Kozhikode"]
        self.buses = self.generate_buses()

    def generate_buses(self):
        """Create a dictionary of buses with unique codes."""
        return {destination: f"BUS-{str(i+1).zfill(3)}" for i, destination in enumerate(self.destinations)}
    
    def show_available_buses(self):
        """Return the available buses with unique codes."""
        return {city: self.buses[city] for city in self.buses}
