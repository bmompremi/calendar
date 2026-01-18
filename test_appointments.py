#!/usr/bin/env python3
"""
Test script to demonstrate the appointment booking functionality
"""

from book_appointment import AppointmentManager

def demo():
    """Demonstrate the appointment booking system"""
    print("🗓️  Appointment Booking System Demo\n")

    # Create a manager instance
    manager = AppointmentManager("demo_appointments.json")

    # Book some sample appointments
    print("Booking sample appointments...\n")

    manager.book_appointment(
        title="Team Meeting",
        date="2025-11-01",
        time="10:00",
        duration=60,
        description="Weekly team sync"
    )

    manager.book_appointment(
        title="Doctor Appointment",
        date="2025-11-05",
        time="14:30",
        duration=30,
        description="Annual checkup"
    )

    manager.book_appointment(
        title="Lunch with Client",
        date="2025-11-03",
        time="12:00",
        duration=90,
        description="Discuss project requirements"
    )

    # List all appointments
    print("\nListing all appointments:")
    manager.list_appointments()

    # Delete an appointment
    print("\nDeleting appointment #2...")
    manager.delete_appointment(2)

    # List appointments after deletion
    print("\nListing appointments after deletion:")
    manager.list_appointments()

if __name__ == "__main__":
    demo()
