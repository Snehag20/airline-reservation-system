import os
import json

class User:
    def __init__(self, username, password, reservations=None):
        self.username = username
        self.password = password
        self.reservations = reservations if reservations is not None else []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "reservations": self.reservations
        }

class Flight:
    def __init__(self, flight_id, origin, destination, seats_available):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.seats_available = seats_available

    def to_dict(self):
        return {
            "flight_id": self.flight_id,
            "origin": self.origin,
            "destination": self.destination,
            "seats_available": self.seats_available
        }

class AirlineReservationSystem:
    def __init__(self):
        self.users = self.load_users()
        self.flights = self.load_flights()

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return [User(**user) for user in json.load(file)]
        return []

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump([user.to_dict() for user in self.users], file)

    def load_flights(self):
        if os.path.exists("flights.json"):
            with open("flights.json", "r") as file:
                return [Flight(**flight) for flight in json.load(file)]
        return []

    def save_flights(self):
        with open("flights.json", "w") as file:
            json.dump([flight.to_dict() for flight in self.flights], file)

    def register_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if any(user.username == username for user in self.users):
            print("Username already exists. Please try again.")
        else:
            self.users.append(User(username, password))
            self.save_users()
            print("Registration successful!")

    def login_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = next((user for user in self.users if user.username == username and user.password == password), None)
        if user:
            print("Login successful!")
            return user
        else:
            print("Invalid username or password.")
            return None

    def add_flight(self):
        flight_id = input("Enter flight ID: ")
        origin = input("Enter origin: ")
        destination = input("Enter destination: ")
        seats_available = int(input("Enter number of seats available: "))
        self.flights.append(Flight(flight_id, origin, destination, seats_available))
        self.save_flights()
        print("Flight added successfully!")

    def view_flights(self):
        if not self.flights:
            print("No flights available.")
            return
        for flight in self.flights:
            print(f"Flight ID: {flight.flight_id}, Origin: {flight.origin}, Destination: {flight.destination}, Seats Available: {flight.seats_available}")

    def book_flight(self, user):
        self.view_flights()
        flight_id = input("Enter flight ID to book: ")
        flight = next((flight for flight in self.flights if flight.flight_id == flight_id), None)
        if flight and flight.seats_available > 0:
            seats = int(input("Enter number of seats to book: "))
            if seats <= flight.seats_available:
                flight.seats_available -= seats
                user.reservations.append({"flight_id": flight_id, "seats": seats})
                self.save_users()
                self.save_flights()
                print("Flight booked successfully!")
            else:
                print("Not enough seats available.")
        else:
            print("Flight not found or no seats available.")

    def view_reservations(self, user):
        if not user.reservations:
            print("No reservations found.")
            return
        for reservation in user.reservations:
            print(f"Flight ID: {reservation['flight_id']}, Seats: {reservation['seats']}")

def main():
    system = AirlineReservationSystem()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Add Flight")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            system.register_user()
        elif choice == "2":
            user = system.login_user()
            if user:
                while True:
                    print("\n1. View Flights")
                    print("2. Book Flight")
                    print("3. View Reservations")
                    print("4. Logout")
                    user_choice = input("Enter choice: ")

                    if user_choice == "1":
                        system.view_flights()
                    elif user_choice == "2":
                        system.book_flight(user)
                    elif user_choice == "3":
                        system.view_reservations(user)
                    elif user_choice == "4":
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            system.add_flight()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
