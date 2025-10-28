# MiConsulado Appointment Booking Bot

Automated booking bot for Mexican Consulate appointments using SeleniumBase.

## Features

- Automated login to MiConsulado portal
- Error handling and retry logic
- Screenshot capture for debugging
- Secure credential management
- Enhanced logging with timestamps

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd calendar

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the template
cp config.py.template config.py

# Edit config.py with your details
nano config.py
```

Fill in your credentials:
```python
EMAIL = "your.email@example.com"
PASSWORD = "your_password"
APPLICANT = "Your Full Name"
SERVICE_TYPE = "passport_renewal"
LOCATION = "San Francisco"
```

### 3. Run

```bash
# Run the improved version (recommended)
python booking_bot_improved.py

# Or run the original version
python booking_bot.py
```

## Files

- `booking_bot.py` - Original version
- `booking_bot_improved.py` - Enhanced version with better error handling
- `config.py.template` - Configuration template
- `REVIEW.md` - Comprehensive code review and recommendations

## Security

- Never commit `config.py` (contains credentials)
- Use strong, unique passwords
- Review MiConsulado's terms of service before automating

## Documentation

See [REVIEW.md](REVIEW.md) for:
- Detailed code review
- Security analysis
- Improvement recommendations
- Future enhancement ideas

## License

MIT License - See LICENSE file for details

## Disclaimer

This bot is for educational and personal use only. Ensure compliance with MiConsulado's terms of service. The authors are not responsible for any misuse.
