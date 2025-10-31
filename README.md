# Banking Management System

A comprehensive banking management system built with Python, featuring customer management, account operations, money transfers, and complete transaction tracking with data persistence.

## Features

### Core Banking Operations
- **Customer Management**: Create and manage customer profiles
- **Account Management**: Multiple account types (Savings, Checking, Business)
- **Deposits & Withdrawals**: Secure money transactions with validation
- **Money Transfers**: Transfer funds between accounts
- **Balance Inquiry**: Check account balances in real-time
- **Transaction History**: Complete audit trail of all operations
- **Data Persistence**: All data saved to JSON for persistence across sessions

### Security Features
- Customer authentication via Customer ID
- Input validation for all operations
- Insufficient funds protection
- Transaction logging and audit trail

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone this repository:
```bash
git clone <repository-url>
cd calendar
```

2. No additional dependencies required - uses Python standard library only!

## Usage

### Running the Application

Start the banking system CLI:
```bash
python3 bank_cli.py
```

Or, if made executable:
```bash
./bank_cli.py
```

### Menu Options

The system provides an interactive menu with the following options:

1. **Create New Customer** - Register a new customer
2. **Login as Customer** - Login with your Customer ID
3. **Create New Account** - Open a new bank account (Savings/Checking/Business)
4. **Deposit Money** - Deposit funds into your account
5. **Withdraw Money** - Withdraw funds from your account
6. **Transfer Money** - Transfer money between accounts
7. **Check Balance** - View your account balance(s)
8. **View Transaction History** - See all past transactions
9. **View Account Details** - Detailed account information
10. **View All Accounts** - List all your accounts
11. **View All Customers** - Admin view of all customers
12. **View Bank Summary** - Bank statistics and summary
13. **Logout** - Logout from current session
0. **Exit** - Close the application

## Quick Start Guide

### 1. Create a Customer
```
Select: 1 (Create New Customer)
Enter name, email, phone, and address
Note down your Customer ID for future login
```

### 2. Login
```
Select: 2 (Login as Customer)
Enter your Customer ID
```

### 3. Create an Account
```
Select: 3 (Create New Account)
Choose account type (Savings/Checking/Business)
Enter initial deposit amount
Note down your Account Number
```

### 4. Make a Deposit
```
Select: 4 (Deposit Money)
Select your account
Enter deposit amount
Add optional description
```

### 5. Check Your Balance
```
Select: 7 (Check Balance)
View all account balances
```

## System Architecture

### Core Classes

#### `Transaction`
- Tracks individual banking transactions
- Records transaction type, amount, timestamp, and description
- Unique transaction ID for each operation

#### `Account`
- Represents a bank account
- Supports deposits, withdrawals, and balance queries
- Maintains transaction history
- Account types: Savings, Checking, Business

#### `Customer`
- Represents a bank customer
- Can hold multiple accounts
- Stores personal information (name, email, phone, address)
- Calculates total balance across all accounts

#### `Bank`
- Central management system
- Handles customer and account creation
- Manages money transfers between accounts
- Provides data persistence via JSON
- Generates unique IDs for customers and accounts

### Data Persistence

All data is automatically saved to `bank_data.json` in the following format:
```json
{
  "name": "Global Banking Corporation",
  "account_counter": 1001,
  "customer_counter": 1001,
  "customers": {
    "CUST00001001": {
      "customer_id": "CUST00001001",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "555-1234",
      "accounts": {
        "ACC00001001": {
          "account_number": "ACC00001001",
          "account_type": "savings",
          "balance": 1000.00,
          "transactions": [...]
        }
      }
    }
  }
}
```

## Example Workflow

```
1. Start the application
   $ python3 bank_cli.py

2. Create a new customer
   Menu: 1
   Name: Alice Smith
   Email: alice@example.com
   Phone: 555-0001
   → Customer ID: CUST00001001

3. Login as customer
   Menu: 2
   Customer ID: CUST00001001

4. Create a savings account
   Menu: 3
   Type: 1 (Savings)
   Initial Deposit: $1000.00
   → Account Number: ACC00001001

5. Make a deposit
   Menu: 4
   Account: 1 (Select ACC00001001)
   Amount: $500.00
   Description: Salary deposit

6. Check balance
   Menu: 7
   → Shows balance: $1500.00

7. Create another customer and transfer money
   Menu: 1
   Create customer: Bob Johnson (CUST00001002)

   Menu: 3
   Create account: ACC00001002

   Menu: 6 (Transfer)
   From: ACC00001001
   To: ACC00001002
   Amount: $200.00
```

## API Usage (Programmatic)

You can also use the banking system programmatically:

```python
from banking_system import Bank

# Initialize bank
bank = Bank("My Bank")

# Create customer
customer = bank.create_customer("John Doe", "john@example.com", "555-1234")

# Create account
account = bank.create_account(customer.customer_id, "savings", 1000.0)

# Deposit money
account.deposit(500.0, "Salary")

# Check balance
print(f"Balance: ${account.get_balance():.2f}")

# Withdraw money
account.withdraw(200.0, "ATM withdrawal")

# View transactions
for transaction in account.get_transaction_history():
    print(transaction)

# Transfer between accounts
bank.transfer(from_account_num, to_account_num, 100.0, "Payment")

# Data is automatically saved to bank_data.json
```

## Error Handling

The system includes comprehensive error handling for:
- Invalid input (non-numeric amounts, invalid choices)
- Insufficient funds
- Account not found
- Customer not found
- Negative deposits/withdrawals
- Invalid account types

## File Structure

```
calendar/
├── banking_system.py    # Core banking system classes
├── bank_cli.py          # Command-line interface
├── bank_data.json       # Persistent data storage (auto-generated)
├── README.md            # This file
└── LICENSE              # License information
```

## Data Storage

- All data is stored in `bank_data.json`
- Data is automatically loaded on startup
- Data is automatically saved after each transaction
- Human-readable JSON format for easy debugging
- No database required

## Features Breakdown

### Account Types
1. **Savings Account** - Standard savings account
2. **Checking Account** - Day-to-day transactions account
3. **Business Account** - For business customers

### Transaction Types
- **Deposit** - Add money to account
- **Withdrawal** - Remove money from account
- **Transfer** - Move money between accounts

### Customer Features
- Unique Customer ID generation
- Multiple accounts per customer
- Total balance calculation across all accounts
- Complete customer profile management

### Banking Features
- Automatic ID generation (Customer & Account)
- Complete audit trail
- Bank-wide statistics and summaries
- Multi-customer support
- Real-time balance updates

## Security Considerations

- Customer authentication required for account operations
- Input validation on all monetary transactions
- Overdraft protection
- Transaction logging for audit purposes
- Data persistence ensures no data loss

## Future Enhancements

Potential features for future versions:
- Interest calculation for savings accounts
- Account statements (PDF export)
- Multi-currency support
- Loan management
- Credit/Debit card management
- Online banking web interface
- Mobile app integration
- Email notifications
- Password/PIN authentication
- Admin panel with user management
- Transaction limits and fraud detection
- Scheduled transfers
- Account closure functionality

## Troubleshooting

### Issue: "Customer not found"
- Solution: Verify Customer ID is correct, check `bank_data.json`

### Issue: "Insufficient funds"
- Solution: Check account balance before withdrawal/transfer

### Issue: Data not persisting
- Solution: Ensure write permissions for `bank_data.json`

### Issue: Invalid input errors
- Solution: Enter numeric values for amounts, valid choices for menus

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

See LICENSE file for details.

## Contact

For support or questions, please open an issue in the repository.

---

**Happy Banking!** 🏦
