from system.book_manager import BookingManager
from admin.admin_manager import AdminManager 
from admin.admin_access import AdminAccess

def main():
    choice = int(input("Hi! user, How can I help you today!\n1. Booking Bus Tickets\n2. Cancelling the Booked tickets\n3. Enter as Admin User\n4. Create Admin User\nEnter you choice: "))
    booking_manager = BookingManager()
    
    if choice == 1:
        booking_manager.book_ticket()
    elif choice == 2:
        booking_manager.cancel_ticket()
    elif choice == 3:
        AdminAccess.get_admin_acces()
    elif choice == 4:
        admin = AdminManager()
        admin.create_admin_user()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
    
    