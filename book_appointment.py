#!/usr/bin/env python3
"""
Calendar Appointment Booking Script
Allows users to book, view, and manage appointments
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# Configuration
APPOINTMENTS_FILE = "appointments.json"


class AppointmentManager:
    """Manages calendar appointments"""

    def __init__(self, filename: str = APPOINTMENTS_FILE):
        self.filename = filename
        self.appointments = self.load_appointments()

    def load_appointments(self) -> List[Dict]:
        """Load appointments from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not read {self.filename}, starting fresh")
                return []
        return []

    def save_appointments(self):
        """Save appointments to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.appointments, f, indent=2)
        print(f"✓ Appointments saved to {self.filename}")

    def book_appointment(self, title: str, date: str, time: str, duration: int, description: str = ""):
        """Book a new appointment"""
        try:
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError as e:
            print(f"Error: Invalid date or time format. {e}")
            return False

        appointment = {
            "id": len(self.appointments) + 1,
            "title": title,
            "date": date,
            "time": time,
            "duration_minutes": duration,
            "description": description,
            "created_at": datetime.now().isoformat()
        }

        self.appointments.append(appointment)
        self.save_appointments()
        print(f"\n✓ Appointment booked successfully!")
        print(f"  ID: {appointment['id']}")
        print(f"  Title: {title}")
        print(f"  Date: {date} at {time}")
        print(f"  Duration: {duration} minutes")
        return True

    def list_appointments(self):
        """List all appointments"""
        if not self.appointments:
            print("No appointments found.")
            return

        print(f"\n{'='*60}")
        print(f"{'APPOINTMENTS':^60}")
        print(f"{'='*60}\n")

        # Sort by date and time
        sorted_appointments = sorted(
            self.appointments,
            key=lambda x: (x['date'], x['time'])
        )

        for apt in sorted_appointments:
            print(f"ID: {apt['id']}")
            print(f"Title: {apt['title']}")
            print(f"Date: {apt['date']} at {apt['time']}")
            print(f"Duration: {apt['duration_minutes']} minutes")
            if apt.get('description'):
                print(f"Description: {apt['description']}")
            print(f"{'-'*60}")

    def delete_appointment(self, appointment_id: int):
        """Delete an appointment by ID"""
        original_length = len(self.appointments)
        self.appointments = [apt for apt in self.appointments if apt['id'] != appointment_id]

        if len(self.appointments) < original_length:
            self.save_appointments()
            print(f"✓ Appointment {appointment_id} deleted successfully!")
            return True
        else:
            print(f"Error: Appointment {appointment_id} not found.")
            return False


def print_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print(" CALENDAR APPOINTMENT BOOKING SYSTEM")
    print("="*60)
    print("1. Book new appointment")
    print("2. View all appointments")
    print("3. Delete appointment")
    print("4. Exit")
    print("="*60)


def main():
    """Main program loop"""
    manager = AppointmentManager()

    print("\n🗓️  Welcome to the Calendar Appointment Booking System!")

    while True:
        print_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            # Book new appointment
            print("\n--- Book New Appointment ---")
            title = input("Title: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            time = input("Time (HH:MM): ").strip()

            try:
                duration = int(input("Duration (minutes): ").strip())
            except ValueError:
                print("Error: Duration must be a number")
                continue

            description = input("Description (optional): ").strip()

            manager.book_appointment(title, date, time, duration, description)

        elif choice == "2":
            # View all appointments
            manager.list_appointments()

        elif choice == "3":
            # Delete appointment
            try:
                apt_id = int(input("\nEnter appointment ID to delete: ").strip())
                manager.delete_appointment(apt_id)
            except ValueError:
                print("Error: Please enter a valid appointment ID")

        elif choice == "4":
            # Exit
            print("\n👋 Thank you for using the Calendar Appointment Booking System!")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
