from system.book_manager import BookingManager

def main():
    choice = int(input("Enter Your choice\n1. Booking Bus Tickets\n2. Cancelling the Booked tickets\n"))
    booking_manager = BookingManager()
    if choice == 1:
        booking_manager.book_ticket()
    elif choice == 2:
        booking_manager.cancel_ticket()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
    
    