#!/usr/bin/env python3
"""MiConsulado Appointment Booking Bot"""
from seleniumbase import SB
import time
from datetime import datetime

try:
    from config import EMAIL, PASSWORD, APPLICANT, SERVICE_TYPE, LOCATION
    print("✓ Config loaded")
except ImportError:
    print("❌ ERROR: config.py not found!")
    exit(1)


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def book():
    log("🇲🇽 Starting booking process...")
    with SB(uc=True, headless=False) as sb:
        log("Opening portal...")
        sb.uc_open_with_reconnect("https://citas.sre.gob.mx/", 4)
        sb.wait_for_element('input[name="usuario"]', timeout=20)
        sb.type('input[name="usuario"]', EMAIL)
        sb.type('input[name="password"]', PASSWORD)
        sb.click('button[type="submit"]')
        sb.wait_for_ready_state_complete()
        log("✓ Login submitted — verify manually")
        sb.save_screenshot("test_booking.png")
        log("✓ Portal opened - check test_booking.png")
        time.sleep(5)
        log("⚠️ This is a test version - full booking not implemented yet")
    return True
