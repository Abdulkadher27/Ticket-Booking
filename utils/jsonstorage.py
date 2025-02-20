import json
import os

class JSONStorage:
    @staticmethod
    def save_json(file_path: str, data: dict | list):
        """Save data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    @staticmethod
    def read_json_file(file_path: str):
        """Static method to read a JSON file and return its content."""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading {file_path}: {e}")
                return None

if __name__ == '__main__':
    pass