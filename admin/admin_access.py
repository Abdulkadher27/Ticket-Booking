from system.book_manager import BookingManager
from system.bus_manager import BusManager
from admin.admin_manager import AdminManager


class AdminAccess:
    
    def get_admin_acces():
        if AdminManager.enter_as_admin():
            choice = int(input("What do you want to update!\n1. Change Number of Seats\n2. Change Amount of Each seats\n3. Add Additional Destination\nEnter Your Choice: "))
            if choice == 1:
                while True:
                    num_seats = int(input("Enter the Number of seats to be Changes: "))
                    if num_seats % 4 != 0:
                        print("Enter the Valid number of Seats!")
                        continue
                    BookingManager.change_num_seats(num_seats)
                    break
            elif choice == 2:
                while True:
                    amount = int(input("Enter the amount to be changes: "))
                    if amount < 0:
                        print("Give Valid Amount!")
                        continue
                    BookingManager.change_seat_amount(amount)
                    break
            elif choice == 3:
                while True:
                    destination = input("Enter the Destination Place: ").strip()
                    if len(destination) < 3:
                        print("Give Proper Place for Destination!")
                        continue
                    busmanager = BusManager()
                    if busmanager.add_destination(destination):
                        print(f"The Destination {destination} is added Successfully!")
                    else:
                        print("Can not Add the Destination")    
                    break
                    
                
                    
        