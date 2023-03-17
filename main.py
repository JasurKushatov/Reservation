import datetime
import csv
import json
import logging

class ReservationSystem:
    def __init__(self):
        self.reservations = {}

    def make_reservation(self):
        name = input("What's your Name? ")

        date_str = input("When would you like to book? {DD.MM.YYYY HH:MM} 19.03.2023 10:00 ")
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M")

        if date < datetime.datetime.now() + datetime.timedelta(hours=1):
            print("Sorry, reservations must be made at least one hour in advance.")
            return

        reservations_this_week = sum(1 for r in self.reservations.values() if r['name'] == name and r['date'].isocalendar()[1] == date.isocalendar()[1])
        if reservations_this_week >= 2:
            print(f"Sorry, {name} has already made {reservations_this_week} reservations this week.")
            return

        available_times = self.get_available_times(date)
        if not available_times:
            print("Sorry, all courts are booked for the specified time.")
            return

        time_str = date.strftime("%H:%M")
        if time_str not in available_times:
            closest_time = min(available_times, key=lambda t: abs((datetime.datetime.strptime(t, "%H:%M") - date).total_seconds()))
            print(f"The time you chose is unavailable, would you like to make a reservation for {closest_time} instead?")
            choice = input("Enter 'yes' or 'no': ")
            if choice.lower() != 'yes':
                return
            date = datetime.datetime.strptime(closest_time, "%H:%M")

        print("How long would you like to book court? ")
        for i, duration in enumerate([30, 60, 90]):
            if date + datetime.timedelta(minutes=duration) > datetime.datetime(date.year, date.month, date.day, 18, 0):
                break
            print(f"{i+1}) {duration} Minutes")
        choice = input("Enter your choice: ")
        duration = [30, 60, 90][int(choice) - 1]
        new_date = date + datetime.timedelta(minutes=duration)
        end_date = new_date.strftime('%d.%m.%Y %H:%M')
        date = date.strftime('%d.%m.%Y %H:%M')
        self.reservations['start_date'] = date
        self.reservations[date_str] = {'name': name, 'date': date, 'end_date': end_date}
        print(f"Reservation made for {name} from {date_str} - till {end_date}.")

    def get_available_times(self, date):
        available_times = set(["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"])
        for r in self.reservations.values():
            if r['date'].date() == date.date():
                available_times.discard(r['date'].strftime("%H:%M"))
                if r['duration'] == 90:
                    available_times.discard((r['date'] + datetime.timedelta(minutes=30)).strftime("%H:%M"))
        return sorted(available_times)

    def cancel_reservation(self):
        date_str = input("Which reservation would you like to cancel? {DD.MM.YYYY HH:MM} ")
        if date_str not in self.reservations:
            print("Sorry, that reservation does not exist.")
            return

        name = self.reservations[date_str]['name']
        del self.reservations[date_str]
        print(f"Reservation for {name} on {date_str} has been cancelled.")

    def print_schedule(self):
        for reservation in self.reservations.values():
            print(f"{reservation}")

    def save_schedule(self):
        users = [
            {"name": "Alice", "start_time": "2022-03-16T09:00:00", "end_time": "2022-03-16T17:00:00"},
            {"name": "Bob", "start_time": "2022-03-16T08:30:00", "end_time": "2022-03-16T16:30:00"},
            {"name": "Charlie", "start_time": "2022-03-16T10:00:00", "end_time": "2022-03-16T18:00:00"}
        ]
       # prompt the user to choose the saving format
        while True:
            choice = input("Choose the saving format (CSV or JSON): ")
            if choice.lower() == 'csv':
                # save the data in CSV format
                with open('data.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(users.__getitem__(0).keys())
                    for i in range(len(users)):
                        writer.writerow(users.__getitem__(i).values())
                print("Data saved in CSV format.")
                break
            elif choice.lower() == 'json':
                # save the data in JSON format
                users = [
                    {"name": "Alice", "start_time": "2022-03-16T09:00:00", "end_time": "2022-03-16T17:00:00"},
                    {"name": "Bob", "start_time": "2022-03-16T08:30:00", "end_time": "2022-03-16T16:30:00"},
                    {"name": "Charlie", "start_time": "2022-03-16T10:00:00", "end_time": "2022-03-16T18:00:00"}
                ]
                with open('data.json', 'w') as f:
                    json.dump(users, f, indent=2)
                print("Data saved in JSON format.")
                break
            else:
                print("Invalid input, please enter 'csv' or 'json'.")


    def run(self):
        while True:
            choice = input("What do you want to do:\n1. Make a reservation\n2. Cancel a reservation\n3. Print schedule\n4. Save schedule to a file\n5. Exit\nEnter your choice: ")
            if choice == '1':
                self.make_reservation()
            elif choice == '2':
                self.cancel_reservation()
            elif choice == '3':
                self.print_schedule()
            elif choice == '4':
                self.save_schedule()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == '__main__':
    system = ReservationSystem()
    system.run()
