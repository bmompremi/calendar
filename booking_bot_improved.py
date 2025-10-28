#!/usr/bin/env python3
"""
MiConsulado Appointment Booking Bot - Improved Version

This is an enhanced version with better error handling, logging,
and security improvements.
"""
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from seleniumbase import SB
except ImportError:
    print("❌ ERROR: seleniumbase not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from config import EMAIL, PASSWORD, APPLICANT, SERVICE_TYPE, LOCATION
    print("✓ Config loaded")
except ImportError:
    print("❌ ERROR: config.py not found!")
    print("📝 Please copy config.py.template to config.py and fill in your details")
    sys.exit(1)


def log(msg, level="INFO"):
    """Enhanced logging with levels"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✓",
        "WARNING": "⚠️",
        "ERROR": "❌"
    }
    icon = icons.get(level, "•")
    print(f"[{timestamp}] {icon} {msg}")


def validate_config():
    """Validate configuration before running"""
    errors = []

    if not EMAIL or EMAIL == "your.email@example.com":
        errors.append("EMAIL not configured")

    if not PASSWORD or PASSWORD == "your_password_here":
        errors.append("PASSWORD not configured")

    if not APPLICANT:
        errors.append("APPLICANT not configured")

    if errors:
        log("Configuration errors found:", "ERROR")
        for error in errors:
            log(f"  - {error}", "ERROR")
        return False

    return True


def safe_click(sb, selector, timeout=10, description="element"):
    """Safely click an element with error handling"""
    try:
        sb.wait_for_element(selector, timeout=timeout)
        sb.click(selector)
        log(f"Clicked {description}", "SUCCESS")
        return True
    except Exception as e:
        log(f"Failed to click {description}: {str(e)}", "ERROR")
        return False


def safe_type(sb, selector, text, timeout=10, description="field"):
    """Safely type into an element with error handling"""
    try:
        sb.wait_for_element(selector, timeout=timeout)
        sb.type(selector, text)
        log(f"Filled {description}", "SUCCESS")
        return True
    except Exception as e:
        log(f"Failed to fill {description}: {str(e)}", "ERROR")
        return False


def take_screenshot(sb, name="screenshot"):
    """Take a screenshot with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{name}_{timestamp}.png"

    # Create screenshots directory if it doesn't exist
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)

    filepath = screenshots_dir / filename
    sb.save_screenshot(str(filepath))
    log(f"Screenshot saved: {filepath}", "SUCCESS")
    return str(filepath)


def login(sb):
    """Handle login process"""
    log("🔐 Logging in...")

    try:
        # Wait for login form
        sb.wait_for_element('input[name="usuario"]', timeout=20)

        # Fill credentials
        if not safe_type(sb, 'input[name="usuario"]', EMAIL, description="email"):
            return False

        if not safe_type(sb, 'input[name="password"]', PASSWORD, description="password"):
            return False

        # Submit form
        if not safe_click(sb, 'button[type="submit"]', description="login button"):
            return False

        # Wait for page to load
        sb.wait_for_ready_state_complete()
        time.sleep(2)  # Additional wait for any redirects

        log("Login submitted successfully", "SUCCESS")
        return True

    except Exception as e:
        log(f"Login failed: {str(e)}", "ERROR")
        return False


def book():
    """Main booking function"""
    log("🇲🇽 Starting MiConsulado booking process...")

    # Validate configuration
    if not validate_config():
        log("Please fix configuration errors before continuing", "ERROR")
        return False

    try:
        with SB(uc=True, headless=False) as sb:
            # Open portal
            log("Opening MiConsulado portal...")
            sb.uc_open_with_reconnect("https://citas.sre.gob.mx/", 4)
            take_screenshot(sb, "01_portal_opened")

            # Login
            if not login(sb):
                take_screenshot(sb, "error_login_failed")
                return False

            take_screenshot(sb, "02_logged_in")

            # TODO: Implement appointment booking flow
            # The following steps would typically include:
            # 1. Navigate to appointment section
            # 2. Select service type
            # 3. Select location
            # 4. Find available dates
            # 5. Select date and time
            # 6. Fill applicant information
            # 7. Confirm booking

            log("⚠️  Full booking flow not yet implemented", "WARNING")
            log("Manual intervention required to complete booking", "WARNING")

            # Keep browser open for manual completion
            input("\nPress Enter to close browser...")

        log("Booking process completed", "SUCCESS")
        return True

    except Exception as e:
        log(f"Booking process failed: {str(e)}", "ERROR")
        return False


def main():
    """Main entry point"""
    try:
        success = book()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("\nProcess interrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        log(f"Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
