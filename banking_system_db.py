"""
Core Banking System for Haiti with Neon Postgres Database
Handles accounts, transactions, and basic banking operations
"""

from datetime import datetime
from typing import List, Optional, Dict
import uuid
from models import Customer, Account, Transaction, BankingSession
from database import DatabaseConnection, DatabaseManager
from config import (
    DEFAULT_CURRENCY, MIN_ACCOUNT_BALANCE, ACCOUNT_TYPES
)


class BankingSystemDB:
    """Main banking system class with database persistence"""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize banking system with database connection

        Args:
            connection_string: PostgreSQL connection string for Neon database
        """
        self.db_conn = DatabaseConnection(connection_string)
        self.db_manager = DatabaseManager(self.db_conn)

    def close(self):
        """Close database connections"""
        self.db_conn.close()

    # ==================== Customer Management ====================

    def create_customer(self, first_name: str, last_name: str, email: str,
                       phone: str, address: str, city: str, country: str,
                       date_of_birth: datetime, national_id: str, password: str) -> Customer:
        """Create a new customer"""
        customer_id = str(uuid.uuid4())
        password_hash = Customer.hash_password(password)

        customer_data = {
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'country': country,
            'date_of_birth': date_of_birth,
            'national_id': national_id,
            'password_hash': password_hash
        }

        # Save to database
        db_customer = self.db_manager.create_customer(customer_data)

        # Convert to Customer object
        customer = Customer(
            customer_id=db_customer['customer_id'],
            first_name=db_customer['first_name'],
            last_name=db_customer['last_name'],
            email=db_customer['email'],
            phone=db_customer['phone'],
            address=db_customer['address'],
            city=db_customer['city'],
            country=db_customer['country'],
            date_of_birth=db_customer['date_of_birth'],
            created_at=db_customer['created_at'],
            national_id=db_customer['national_id'],
            password_hash=db_customer['password_hash']
        )

        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        db_customer = self.db_manager.get_customer_by_id(customer_id)
        if not db_customer:
            return None

        return Customer(
            customer_id=db_customer['customer_id'],
            first_name=db_customer['first_name'],
            last_name=db_customer['last_name'],
            email=db_customer['email'],
            phone=db_customer['phone'],
            address=db_customer['address'],
            city=db_customer['city'],
            country=db_customer['country'],
            date_of_birth=db_customer['date_of_birth'],
            created_at=db_customer['created_at'],
            national_id=db_customer['national_id'],
            password_hash=db_customer['password_hash']
        )

    def authenticate_customer(self, email: str, password: str) -> Optional[Customer]:
        """Authenticate a customer"""
        db_customer = self.db_manager.get_customer_by_email(email)
        if not db_customer:
            return None

        customer = Customer(
            customer_id=db_customer['customer_id'],
            first_name=db_customer['first_name'],
            last_name=db_customer['last_name'],
            email=db_customer['email'],
            phone=db_customer['phone'],
            address=db_customer['address'],
            city=db_customer['city'],
            country=db_customer['country'],
            date_of_birth=db_customer['date_of_birth'],
            created_at=db_customer['created_at'],
            national_id=db_customer['national_id'],
            password_hash=db_customer['password_hash']
        )

        if customer.verify_password(password):
            return customer
        return None

    # ==================== Account Management ====================

    def create_account(self, customer_id: str, account_type: str,
                      initial_deposit: float = 0.0,
                      currency: str = DEFAULT_CURRENCY) -> Optional[Account]:
        """Create a new bank account"""
        # Validate customer exists
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        if account_type not in ACCOUNT_TYPES:
            raise ValueError(f"Invalid account type. Must be one of: {ACCOUNT_TYPES}")

        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")

        # Create account in database
        account_data = {
            'customer_id': customer_id,
            'account_type': account_type,
            'balance': initial_deposit,
            'currency': currency,
            'status': 'ACTIVE'
        }

        db_account = self.db_manager.create_account(account_data)

        # Convert to Account object
        account = Account(
            account_number=db_account['account_number'],
            customer_id=db_account['customer_id'],
            account_type=db_account['account_type'],
            balance=float(db_account['balance']),
            currency=db_account['currency'],
            status=db_account['status'],
            created_at=db_account['created_at'],
            updated_at=db_account['updated_at'],
            daily_transfer_total=float(db_account['daily_transfer_total']),
            last_transfer_date=db_account['last_transfer_date']
        )

        # Record initial deposit if any
        if initial_deposit > 0:
            self._record_transaction(
                from_account=None,
                to_account=account.account_number,
                amount=initial_deposit,
                currency=currency,
                transaction_type="DEPOSIT",
                description="Initial deposit"
            )

        return account

    def get_account(self, account_number: str) -> Optional[Account]:
        """Get account by account number"""
        db_account = self.db_manager.get_account(account_number)
        if not db_account:
            return None

        return Account(
            account_number=db_account['account_number'],
            customer_id=db_account['customer_id'],
            account_type=db_account['account_type'],
            balance=float(db_account['balance']),
            currency=db_account['currency'],
            status=db_account['status'],
            created_at=db_account['created_at'],
            updated_at=db_account['updated_at'],
            daily_transfer_total=float(db_account['daily_transfer_total']),
            last_transfer_date=db_account['last_transfer_date']
        )

    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        """Get all accounts for a customer"""
        db_accounts = self.db_manager.get_customer_accounts(customer_id)

        return [
            Account(
                account_number=acc['account_number'],
                customer_id=acc['customer_id'],
                account_type=acc['account_type'],
                balance=float(acc['balance']),
                currency=acc['currency'],
                status=acc['status'],
                created_at=acc['created_at'],
                updated_at=acc['updated_at'],
                daily_transfer_total=float(acc['daily_transfer_total']),
                last_transfer_date=acc['last_transfer_date']
            )
            for acc in db_accounts
        ]

    def get_account_balance(self, account_number: str) -> Optional[float]:
        """Get account balance"""
        account = self.get_account(account_number)
        return account.balance if account else None

    # ==================== Transaction Operations ====================

    def deposit(self, account_number: str, amount: float,
               description: str = "Deposit") -> tuple[bool, str, Optional[Transaction]]:
        """Deposit money into an account"""
        if amount <= 0:
            return False, "Deposit amount must be positive", None

        account = self.get_account(account_number)
        if not account:
            return False, "Account not found", None

        if account.status != "ACTIVE":
            return False, f"Account is {account.status}", None

        # Update balance in database
        new_balance = account.balance + amount
        self.db_manager.update_account_balance(account_number, new_balance)

        # Record transaction
        transaction = self._record_transaction(
            from_account=None,
            to_account=account_number,
            amount=amount,
            currency=account.currency,
            transaction_type="DEPOSIT",
            description=description
        )

        return True, f"Successfully deposited {account.currency} {amount:,.2f}", transaction

    def withdraw(self, account_number: str, amount: float,
                description: str = "Withdrawal") -> tuple[bool, str, Optional[Transaction]]:
        """Withdraw money from an account"""
        if amount <= 0:
            return False, "Withdrawal amount must be positive", None

        account = self.get_account(account_number)
        if not account:
            return False, "Account not found", None

        if account.status != "ACTIVE":
            return False, f"Account is {account.status}", None

        if account.balance < amount:
            return False, "Insufficient funds", None

        if account.balance - amount < MIN_ACCOUNT_BALANCE:
            return False, f"Withdrawal would bring balance below minimum ({MIN_ACCOUNT_BALANCE})", None

        # Update balance in database
        new_balance = account.balance - amount
        self.db_manager.update_account_balance(account_number, new_balance)

        # Record transaction
        transaction = self._record_transaction(
            from_account=account_number,
            to_account=None,
            amount=amount,
            currency=account.currency,
            transaction_type="WITHDRAWAL",
            description=description
        )

        return True, f"Successfully withdrew {account.currency} {amount:,.2f}", transaction

    def _record_transaction(self, from_account: Optional[str], to_account: Optional[str],
                           amount: float, currency: str, transaction_type: str,
                           description: str, fee: float = 0.0,
                           exchange_rate: float = 1.0) -> Transaction:
        """Internal method to record a transaction"""
        transaction_id = str(uuid.uuid4())
        reference_number = f"TXN-{transaction_id[:8]}"

        transaction_data = {
            'transaction_id': transaction_id,
            'from_account': from_account,
            'to_account': to_account,
            'amount': amount,
            'currency': currency,
            'transaction_type': transaction_type,
            'status': 'COMPLETED',
            'description': description,
            'fee': fee,
            'exchange_rate': exchange_rate,
            'reference_number': reference_number
        }

        # Save to database
        db_transaction = self.db_manager.create_transaction(transaction_data)

        # Convert to Transaction object
        transaction = Transaction(
            transaction_id=db_transaction['transaction_id'],
            from_account=db_transaction['from_account'],
            to_account=db_transaction['to_account'],
            amount=float(db_transaction['amount']),
            currency=db_transaction['currency'],
            transaction_type=db_transaction['transaction_type'],
            status=db_transaction['status'],
            timestamp=db_transaction['timestamp'],
            description=db_transaction['description'],
            fee=float(db_transaction['fee']),
            exchange_rate=float(db_transaction['exchange_rate']),
            reference_number=db_transaction['reference_number']
        )

        return transaction

    def get_account_transactions(self, account_number: str,
                                 limit: int = 10) -> List[Transaction]:
        """Get recent transactions for an account"""
        db_transactions = self.db_manager.get_account_transactions(account_number, limit)

        return [
            Transaction(
                transaction_id=txn['transaction_id'],
                from_account=txn['from_account'],
                to_account=txn['to_account'],
                amount=float(txn['amount']),
                currency=txn['currency'],
                transaction_type=txn['transaction_type'],
                status=txn['status'],
                timestamp=txn['timestamp'],
                description=txn['description'],
                fee=float(txn['fee']),
                exchange_rate=float(txn['exchange_rate']),
                reference_number=txn['reference_number']
            )
            for txn in db_transactions
        ]

    def get_account_statement(self, account_number: str,
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> List[Transaction]:
        """Get account statement for a date range"""
        if not start_date:
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        if not end_date:
            end_date = datetime.now()

        db_transactions = self.db_manager.get_account_statement(
            account_number, start_date, end_date
        )

        return [
            Transaction(
                transaction_id=txn['transaction_id'],
                from_account=txn['from_account'],
                to_account=txn['to_account'],
                amount=float(txn['amount']),
                currency=txn['currency'],
                transaction_type=txn['transaction_type'],
                status=txn['status'],
                timestamp=txn['timestamp'],
                description=txn['description'],
                fee=float(txn['fee']),
                exchange_rate=float(txn['exchange_rate']),
                reference_number=txn['reference_number']
            )
            for txn in db_transactions
        ]

    # ==================== Session Management ====================

    def create_session(self, customer_id: str) -> BankingSession:
        """Create a new banking session"""
        session_id = str(uuid.uuid4())
        session_data = {
            'session_id': session_id,
            'customer_id': customer_id
        }

        db_session = self.db_manager.create_session(session_data)

        session = BankingSession(
            session_id=db_session['session_id'],
            customer_id=db_session['customer_id'],
            login_time=db_session['login_time'],
            last_activity=db_session['last_activity'],
            is_active=db_session['is_active']
        )

        return session

    def validate_session(self, session_id: str) -> Optional[BankingSession]:
        """Validate and return an active session"""
        db_session = self.db_manager.get_session(session_id)
        if not db_session:
            return None

        session = BankingSession(
            session_id=db_session['session_id'],
            customer_id=db_session['customer_id'],
            login_time=db_session['login_time'],
            last_activity=db_session['last_activity'],
            is_active=db_session['is_active']
        )

        if session.is_expired():
            self.end_session(session_id)
            return None

        # Update last activity
        self.db_manager.update_session_activity(session_id)
        session.last_activity = datetime.now()

        return session

    def end_session(self, session_id: str) -> bool:
        """End a banking session"""
        rows = self.db_manager.end_session(session_id)
        return rows > 0
