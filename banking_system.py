"""
Core Banking System for Haiti
Handles accounts, transactions, and basic banking operations
"""

from datetime import datetime
from typing import List, Optional, Dict
import uuid
from models import Customer, Account, Transaction, TransferRequest, BankingSession
from config import (
    DEFAULT_CURRENCY, EXCHANGE_RATES, MAX_DAILY_TRANSFER_LIMIT,
    MAX_SINGLE_TRANSFER_LIMIT, MIN_TRANSFER_AMOUNT, MIN_ACCOUNT_BALANCE,
    INITIAL_ACCOUNT_NUMBER, ACCOUNT_TYPES, TRANSACTION_TYPES
)


class BankingSystem:
    """Main banking system class"""

    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[Transaction] = []
        self.sessions: Dict[str, BankingSession] = {}
        self.next_account_number = INITIAL_ACCOUNT_NUMBER

    # ==================== Customer Management ====================

    def create_customer(self, first_name: str, last_name: str, email: str,
                       phone: str, address: str, city: str, country: str,
                       date_of_birth: datetime, national_id: str, password: str) -> Customer:
        """Create a new customer"""
        customer_id = str(uuid.uuid4())
        password_hash = Customer.hash_password(password)

        customer = Customer(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
            date_of_birth=date_of_birth,
            created_at=datetime.now(),
            national_id=national_id,
            password_hash=password_hash
        )

        self.customers[customer_id] = customer
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        return self.customers.get(customer_id)

    def authenticate_customer(self, email: str, password: str) -> Optional[Customer]:
        """Authenticate a customer"""
        for customer in self.customers.values():
            if customer.email == email and customer.verify_password(password):
                return customer
        return None

    # ==================== Account Management ====================

    def create_account(self, customer_id: str, account_type: str,
                      initial_deposit: float = 0.0,
                      currency: str = DEFAULT_CURRENCY) -> Optional[Account]:
        """Create a new bank account"""
        if customer_id not in self.customers:
            raise ValueError("Customer not found")

        if account_type not in ACCOUNT_TYPES:
            raise ValueError(f"Invalid account type. Must be one of: {ACCOUNT_TYPES}")

        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")

        account_number = str(self.next_account_number)
        self.next_account_number += 1

        account = Account(
            account_number=account_number,
            customer_id=customer_id,
            account_type=account_type,
            balance=initial_deposit,
            currency=currency,
            status="ACTIVE",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.accounts[account_number] = account

        # Record initial deposit if any
        if initial_deposit > 0:
            self._record_transaction(
                from_account=None,
                to_account=account_number,
                amount=initial_deposit,
                currency=currency,
                transaction_type="DEPOSIT",
                description="Initial deposit"
            )

        return account

    def get_account(self, account_number: str) -> Optional[Account]:
        """Get account by account number"""
        return self.accounts.get(account_number)

    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        """Get all accounts for a customer"""
        return [acc for acc in self.accounts.values() if acc.customer_id == customer_id]

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

        # Update balance
        account.balance += amount
        account.updated_at = datetime.now()

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

        # Update balance
        account.balance -= amount
        account.updated_at = datetime.now()

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
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            status="COMPLETED",
            timestamp=datetime.now(),
            description=description,
            fee=fee,
            exchange_rate=exchange_rate
        )

        self.transactions.append(transaction)
        return transaction

    def get_account_transactions(self, account_number: str,
                                 limit: int = 10) -> List[Transaction]:
        """Get recent transactions for an account"""
        transactions = [
            t for t in self.transactions
            if t.from_account == account_number or t.to_account == account_number
        ]
        # Sort by timestamp, most recent first
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions[:limit]

    def get_account_statement(self, account_number: str,
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> List[Transaction]:
        """Get account statement for a date range"""
        transactions = [
            t for t in self.transactions
            if t.from_account == account_number or t.to_account == account_number
        ]

        if start_date:
            transactions = [t for t in transactions if t.timestamp >= start_date]
        if end_date:
            transactions = [t for t in transactions if t.timestamp <= end_date]

        transactions.sort(key=lambda x: x.timestamp)
        return transactions

    # ==================== Session Management ====================

    def create_session(self, customer_id: str) -> BankingSession:
        """Create a new banking session"""
        session_id = str(uuid.uuid4())
        session = BankingSession(
            session_id=session_id,
            customer_id=customer_id,
            login_time=datetime.now(),
            last_activity=datetime.now()
        )
        self.sessions[session_id] = session
        return session

    def validate_session(self, session_id: str) -> Optional[BankingSession]:
        """Validate and return an active session"""
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            session.last_activity = datetime.now()
            return session
        return None

    def end_session(self, session_id: str) -> bool:
        """End a banking session"""
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False
            return True
        return False
