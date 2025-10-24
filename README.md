# Haiti National Bank - Money Transfer System

A complete web-based banking system for Haiti with secure money transfer functionality.

## Features

- **User Authentication**: Secure registration and login system
- **Account Management**: Create and manage multiple checking and savings accounts
- **Money Transfers**: Transfer money between accounts with real-time validation
- **Transaction History**: Complete audit trail of all transactions
- **Multi-Currency Support**: Built for Haitian Gourde (HTG)
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask 3.0.0 (Python)
- **Database**: SQLAlchemy with support for SQLite, PostgreSQL, MySQL
- **Authentication**: Flask-Login with secure password hashing
- **Frontend**: HTML5, CSS3, JavaScript

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd calendar
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Initialize the database:
```bash
flask init-db
flask seed-db  # Optional: Creates admin user (admin/admin123)
```

6. Run the application:
```bash
python app.py
```

7. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Credentials (if using seed-db)

- **Username**: admin
- **Password**: admin123

## Configuration

### Environment Variables

- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: development or production

### Transfer Limits

- Minimum: G 1.00
- Maximum: G 1,000,000.00

## Database Support

### SQLite (Default)
```
DATABASE_URL=sqlite:///haiti_bank.db
```

### PostgreSQL
```
DATABASE_URL=postgresql://username:password@localhost/haiti_bank
```

### MySQL
```
DATABASE_URL=mysql://username:password@localhost/haiti_bank
```

## API Endpoints

### Account Verification
```
GET /api/account/<account_number>
```

Returns account information if the account exists and is active.

## Project Structure

```
calendar/
├── app.py                 # Main application file
├── models.py             # Database models
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── accounts.html
│   ├── create_account.html
│   ├── transfer.html
│   ├── transactions.html
│   └── profile.html
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection
- Input validation
- Balance verification before transfers
- Account number format validation

## Usage Guide

### Creating an Account

1. Register a new user account
2. Login with your credentials
3. Navigate to "Accounts" > "Create Account"
4. Select account type (Checking or Savings)
5. Your account will be created with a unique 16-digit account number

### Making a Transfer

1. Navigate to "Transfer"
2. Select your source account
3. Enter recipient's account number
4. Enter transfer amount
5. Add optional description
6. Submit transfer

The system will:
- Verify recipient account exists
- Check sufficient balance
- Validate transfer amount
- Process transfer instantly
- Create transaction record

### Viewing Transactions

Navigate to "Transactions" to view:
- Complete transaction history
- Transaction IDs
- Dates and times
- Sender and recipient accounts
- Amounts and descriptions
- Transaction status

## CLI Commands

```bash
# Initialize database
flask init-db

# Seed database with admin user
flask seed-db
```

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

---

**Haiti National Bank** - Your trusted banking partner
