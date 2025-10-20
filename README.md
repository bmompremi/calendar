# Haiti Banking Management System
### Sistèm Jesyon Bankè Ayiti

A comprehensive banking management system with money transfer capabilities designed specifically for Haiti. This system supports both domestic and international money transfers with support for Haitian Gourde (HTG) and US Dollar (USD) currencies.

## Features

### Core Banking Features
- **Customer Management**: Register and authenticate customers with secure password hashing
- **Account Management**: Create and manage multiple account types (Savings, Checking, Business)
- **Deposits & Withdrawals**: Full support for account deposits and withdrawals
- **Balance Tracking**: Real-time balance updates and account status monitoring
- **Multi-Currency Support**: Support for HTG (Haitian Gourde) and USD with automatic conversion

### Money Transfer System
- **Domestic Transfers**: Transfer money between accounts within the same bank
- **International Transfers**: Send money to international banks with currency conversion
- **Transfer Limits**: Daily and single transaction limits for security
- **Transfer Fees**: Automatic fee calculation (1% domestic, 2.5% international)
- **Transaction History**: Complete audit trail of all transactions
- **Real-time Validation**: Balance checks, daily limit enforcement, and status verification

### Security Features
- **Password Hashing**: Secure password storage using bcrypt
- **Session Management**: Time-based session expiration
- **Account Status Control**: Ability to suspend or close accounts
- **Transaction Validation**: Comprehensive validation for all operations
- **Daily Limits**: Configurable daily transfer limits to prevent fraud

### Haiti-Specific Features
- **HTG Currency Support**: Native support for Haitian Gourde
- **Local Bank Integration**: Support for major Haitian banks (BNC, Sogebank, Unibank, BPH, etc.)
- **National ID Support**: Customer registration with Haitian National ID
- **Bilingual Interface**: English and Haitian Creole support

## System Architecture

```
haiti-banking-system/
├── config.py              # Configuration settings (currencies, limits, banks)
├── models.py              # Data models (Customer, Account, Transaction)
├── banking_system.py      # Core banking operations
├── transfer_system.py     # Money transfer functionality
├── main.py                # CLI interface
├── demo.py                # Demo/testing script
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd calendar

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the CLI Application

```bash
python main.py
```

### Running the Demo

```bash
python demo.py
```

The demo script demonstrates all features of the system including:
- Customer registration
- Account creation
- Deposits and withdrawals
- Domestic and international transfers
- Transaction history
- Authentication

## Quick Start Guide

### 1. Register a Customer

```python
from datetime import datetime
from banking_system import BankingSystem

banking_system = BankingSystem()

customer = banking_system.create_customer(
    first_name="Jean",
    last_name="Baptiste",
    email="jean@example.ht",
    phone="+509-1234-5678",
    address="123 Rue de la République",
    city="Port-au-Prince",
    country="Haiti",
    date_of_birth=datetime(1985, 3, 15),
    national_id="NIF-001234567",
    password="secure_password"
)
```

### 2. Create an Account

```python
account = banking_system.create_account(
    customer_id=customer.customer_id,
    account_type="CHECKING",
    initial_deposit=50000.00,
    currency="HTG"
)
```

### 3. Deposit Money

```python
success, message, transaction = banking_system.deposit(
    account.account_number,
    25000.00,
    "Salary deposit"
)
```

### 4. Transfer Money (Domestic)

```python
from transfer_system import TransferSystem

transfer_system = TransferSystem(banking_system)

success, message, transaction = transfer_system.transfer_domestic(
    from_account_number="1000000",
    to_account_number="1000001",
    amount=10000.00,
    description="Payment for services"
)
```

### 5. Transfer Money (International)

```python
success, message, transaction = transfer_system.transfer_international(
    from_account_number="1000000",
    recipient_name="John Smith",
    recipient_bank="Bank of America",
    recipient_account="987654321",
    amount=13200.00,  # HTG
    currency="USD",
    description="Family remittance"
)
```

### 6. View Transaction History

```python
transactions = banking_system.get_account_transactions(
    account_number="1000000",
    limit=10
)

for txn in transactions:
    print(f"{txn.reference_number}: {txn.transaction_type} - {txn.amount:,.2f}")
```

## Configuration

### Currency Settings
Default currency is HTG (Haitian Gourde). Exchange rates are configured in `config.py`:
- 1 USD ≈ 132 HTG (configurable)

### Transfer Limits
- Maximum single transfer: 100,000 HTG
- Maximum daily transfer: 500,000 HTG
- Minimum transfer amount: 10 HTG

### Transaction Fees
- Domestic transfers: 1% (min 5 HTG, max 500 HTG)
- International transfers: 2.5% (min 5 HTG, max 500 HTG)

### Supported Banks
The system includes support for major Haitian banks:
- Banque de la République d'Haïti (BRH)
- Banque Nationale de Crédit (BNC)
- Capital Bank
- Sogebank
- Unibank
- Banque Populaire Haïtienne (BPH)
- Citibank Haiti
- Banque de l'Union Haïtienne (BUH)

## Account Types

1. **SAVINGS**: Personal savings account
2. **CHECKING**: Personal checking account
3. **BUSINESS**: Business account

## Transaction Types

- **DEPOSIT**: Money deposited into account
- **WITHDRAWAL**: Money withdrawn from account
- **TRANSFER_SENT**: Outgoing transfer
- **TRANSFER_RECEIVED**: Incoming transfer
- **TRANSFER_INTERNATIONAL**: International transfer

## API Reference

### BankingSystem Class

#### Customer Management
- `create_customer(...)` - Register a new customer
- `get_customer(customer_id)` - Retrieve customer details
- `authenticate_customer(email, password)` - Authenticate a customer

#### Account Management
- `create_account(...)` - Create a new bank account
- `get_account(account_number)` - Get account details
- `get_customer_accounts(customer_id)` - Get all accounts for a customer
- `get_account_balance(account_number)` - Get current balance

#### Transaction Operations
- `deposit(account_number, amount, description)` - Deposit money
- `withdraw(account_number, amount, description)` - Withdraw money
- `get_account_transactions(account_number, limit)` - Get transaction history
- `get_account_statement(account_number, start_date, end_date)` - Get statement

#### Session Management
- `create_session(customer_id)` - Create authenticated session
- `validate_session(session_id)` - Validate existing session
- `end_session(session_id)` - End session

### TransferSystem Class

#### Transfer Operations
- `transfer_domestic(from_account, to_account, amount, description)` - Domestic transfer
- `transfer_international(from_account, recipient_name, recipient_bank, ...)` - International transfer
- `get_transfer_history(account_number, days)` - Get transfer history
- `get_daily_transfer_summary(account_number)` - Get daily transfer summary

#### Utility Methods
- `calculate_transfer_fee(amount, transfer_type)` - Calculate transfer fee
- `check_daily_limit(account_number, amount)` - Verify daily limits

## Security Considerations

1. **Password Security**: All passwords are hashed using bcrypt
2. **Session Timeout**: Sessions expire after 30 minutes of inactivity
3. **Transfer Limits**: Daily and single transaction limits prevent large unauthorized transfers
4. **Account Status**: Accounts can be suspended or closed to prevent unauthorized access
5. **Transaction Validation**: All transactions are validated before execution

## Error Handling

The system provides comprehensive error messages for:
- Insufficient funds
- Invalid account numbers
- Exceeded transfer limits
- Invalid credentials
- Account status issues
- Invalid amounts

## Testing

Run the demo script to test all features:

```bash
python demo.py
```

The demo creates sample customers, performs various transactions, and displays results.

## Future Enhancements

Potential features for future versions:
- Mobile money integration (Moncash, Natcash)
- Loan management system
- Interest calculation for savings accounts
- Multi-factor authentication
- SMS/Email notifications
- API REST interface
- Database persistence (currently in-memory)
- Account statements export (PDF, CSV)
- Scheduled/recurring transfers
- Integration with international remittance services

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

See LICENSE file for details.

## Contact

For questions or support, please contact the development team.

---

**Sistèm Bankè sa a kreye espesyalman pou Haiti ak bezwen pèp ayisyen yo.** (This banking system is created especially for Haiti and the needs of the Haitian people.)
