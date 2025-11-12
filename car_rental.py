from datetime import datetime, timedelta
import math


class Vehicle:
    def __init__(self, make, model, year, rate_hourly, rate_daily, rate_weekly, stock):
        self.make = make
        self.model = model
        self.year = year
        self.rate_hourly = rate_hourly
        self.rate_daily = rate_daily
        self.rate_weekly = rate_weekly
        self.stock = stock
        self.rented = 0


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class CarRental:
    def __init__(self):
        self.stock = {
            'Sedan': Vehicle('Toyota', 'Camry', 2022, 10, 50, 200, 10),
            'SUV': Vehicle('Honda', 'CRV', 2022, 15, 70, 300, 8),
            'Hatchback': Vehicle('Ford', 'Fiesta', 2022, 8, 40, 150, 12)
        }
        self.rental_records = {}
        self.customers = {}

    # Display available cars
    def display_available_cars(self):
        print("\nAvailable Cars:")
        for vehicle_type, vehicle in self.stock.items():
            print(f"{vehicle_type}: {vehicle.stock - vehicle.rented} available")

    # Generic rental handler
    def _rent_vehicle(self, vehicle_type, num_cars, rental_time, rate, period_name, delta, customer):
        vehicle = self.stock.get(vehicle_type)
        if vehicle and 0 < num_cars <= (vehicle.stock - vehicle.rented):
            vehicle.rented += num_cars
            rental_end_time = rental_time + delta
            self.rental_records[rental_time] = (
                vehicle_type, num_cars, rate, rental_time, rental_end_time
            )
            self.customers[customer.email] = customer
            print(f"{num_cars} {vehicle_type}(s) rented {period_name} at {rental_time} by {customer.name}.")
        else:
            print("❌ Sorry, not enough cars available for that type or invalid number of cars.")

    def rent_hourly(self, vehicle_type, num_cars, rental_time, customer):
        self._rent_vehicle(vehicle_type, num_cars, rental_time,
                           self.stock[vehicle_type].rate_hourly, "hourly", timedelta(hours=1), customer)

    def rent_daily(self, vehicle_type, num_cars, rental_time, customer):
        self._rent_vehicle(vehicle_type, num_cars, rental_time,
                           self.stock[vehicle_type].rate_daily, "daily", timedelta(days=1), customer)

    def rent_weekly(self, vehicle_type, num_cars, rental_time, customer):
        self._rent_vehicle(vehicle_type, num_cars, rental_time,
                           self.stock[vehicle_type].rate_weekly, "weekly", timedelta(weeks=1), customer)

    # Return cars and calculate bill
    def return_cars(self, return_time):
        found = False
        for key, value in list(self.rental_records.items()):
            vehicle_type, num_cars, rate, rent_start_time, rent_end_time = value

            # Fix: Check if rental has ended
            if return_time >= rent_start_time:
                found = True
                vehicle = self.stock.get(vehicle_type)
                vehicle.rented -= num_cars
                self.rental_records.pop(key)

                rental_period_hours = (return_time - rent_start_time).total_seconds() / 3600
                total_units = max(1, math.ceil(rental_period_hours))  # at least one billing unit
                total_amount = num_cars * rate * total_units

                print(f"✅ {num_cars} {vehicle_type}(s) returned.")
                print(f"🕓 Rental Duration: {total_units:.0f} hour(s)")
                print(f"💰 Total Bill: ₹{total_amount:.2f}\n")

        if not found:
            print("⚠️ No rental record found for the given return time.")


# Optional: simple test driver (only runs if executed directly)
if __name__ == "__main__":
    rental_service = CarRental()
    customer = Customer("John Doe", "john@example.com")

    rental_service.display_available_cars()
    start_time = datetime.now()

    rental_service.rent_hourly("Sedan", 2, start_time, customer)
    rental_service.display_available_cars()

    # simulate returning after 2 hours
    return_time = start_time + timedelta(hours=2)
    rental_service.return_cars(return_time)
    rental_service.display_available_cars()
