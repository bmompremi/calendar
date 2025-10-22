# Haiti Banking System 2.0

A comprehensive web-based banking system built for Haiti with money transfer capabilities, account management, and transaction tracking.

## Features

- **User Authentication**: Secure registration and login system
- **Account Management**: Create and manage multiple accounts (Checking & Savings)
- **Money Transfers**: Instant transfers between accounts with validation
- **Transaction History**: Complete audit trail of all transactions
- **User Profiles**: Manage personal information
- **Multi-Currency Support**: Built for Haitian Gourde (HTG)
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Validation**: Account verification and balance checks

## Technology Stack

- **Backend**: Python 3.x with Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: Password hashing with Werkzeug

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calendar
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. **Initialize the database**
   ```bash
   flask init-db
   ```

6. **Seed the database (Optional)**
   ```bash
   flask seed-db
   ```
   This creates an admin user:
   - Username: `admin`
   - Password: `admin123`

## Running the Application

1. **Start the development server**
   ```bash
   python app.py
   ```

2. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Creating an Account

1. Click "Register" on the homepage
2. Fill in your personal information
3. Submit the form
4. A default checking account will be created automatically

### Making a Transfer

1. Login to your account
2. Navigate to "Transfer" in the menu
3. Select your source account
4. Enter the recipient's account number
5. Specify the amount and description
6. Confirm the transfer

### Viewing Transactions

1. Go to "Transactions" in the menu
2. View all your transaction history
3. See detailed information about each transaction

## Project Structure

```
calendar/
├── app.py                  # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
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
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── haiti_bank.db        # SQLite database (created on first run)
```

## Features Details

### Account Types

- **Checking Account**: For daily transactions with no minimum balance
- **Savings Account**: For saving money with interest (future feature)

### Transfer Limits

- Minimum transfer: G 1.00
- Maximum transfer: G 1,000,000.00

### Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection
- Input validation and sanitization
- Balance verification before transfers

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard & Accounts
- `GET /dashboard` - User dashboard
- `GET /accounts` - List all accounts
- `GET/POST /accounts/create` - Create new account

### Transfers & Transactions
- `GET/POST /transfer` - Money transfer
- `GET /transactions` - Transaction history

### User Profile
- `GET /profile` - View profile
- `POST /profile/update` - Update profile

### API
- `GET /api/account/<account_number>` - Get account details

## Development

### Database Models

1. **User**: Stores user information and credentials
2. **Account**: Bank accounts with balances
3. **Transaction**: Transfer records and history

### Adding New Features

To add new features:
1. Update models in `models.py` if needed
2. Add routes in `app.py`
3. Create templates in `templates/`
4. Update styles in `static/css/style.css`

## Testing

To test the system:

1. Register a new user
2. Create multiple accounts
3. Perform transfers between accounts
4. Check transaction history
5. Update profile information

## Production Deployment

For production deployment:

1. Change `SECRET_KEY` to a strong random value
2. Use a production database (PostgreSQL recommended)
3. Set `FLASK_ENV=production`
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Enable HTTPS
6. Set up proper logging
7. Configure backups

## Troubleshooting

### Database Issues
```bash
# Reset database
rm haiti_bank.db
flask init-db
flask seed-db
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## Version History

### Version 2.0 (Current)
- Complete rewrite with modern architecture
- Enhanced UI/UX with responsive design
- Improved security features
- Transaction history and reporting
- Multi-account support
- Profile management

## Acknowledgments

- Built for the people of Haiti
- Designed with security and usability in mind
- Uses industry-standard banking practices
