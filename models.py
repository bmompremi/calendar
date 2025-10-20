"""
Data models for Haiti Banking Management System
"""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
import bcrypt
import uuid


@dataclass
class Customer:
    """Represents a bank customer"""
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    country: str
    date_of_birth: datetime
    created_at: datetime
    national_id: str  # Haiti National ID
    password_hash: str = ""

    def __post_init__(self):
        if not self.password_hash:
            raise ValueError("Password hash is required")

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_full_name(self) -> str:
        """Get customer's full name"""
        return f"{self.first_name} {self.last_name}"


@dataclass
class Account:
    """Represents a bank account"""
    account_number: str
    customer_id: str
    account_type: str  # SAVINGS, CHECKING, BUSINESS
    balance: float
    currency: str
    status: str  # ACTIVE, SUSPENDED, CLOSED
    created_at: datetime
    updated_at: datetime
    daily_transfer_total: float = 0.0
    last_transfer_date: Optional[datetime] = None

    def __str__(self):
        return f"Account {self.account_number} - {self.account_type} - {self.currency} {self.balance:,.2f}"


@dataclass
class Transaction:
    """Represents a financial transaction"""
    transaction_id: str
    from_account: Optional[str]  # None for deposits
    to_account: Optional[str]  # None for withdrawals
    amount: float
    currency: str
    transaction_type: str  # DEPOSIT, WITHDRAWAL, TRANSFER_SENT, TRANSFER_RECEIVED, TRANSFER_INTERNATIONAL
    status: str  # PENDING, COMPLETED, FAILED, CANCELLED
    timestamp: datetime
    description: str
    fee: float = 0.0
    exchange_rate: float = 1.0
    reference_number: str = ""

    def __post_init__(self):
        if not self.reference_number:
            self.reference_number = f"TXN-{self.transaction_id[:8]}"

    def __str__(self):
        return f"{self.reference_number}: {self.transaction_type} - {self.currency} {self.amount:,.2f}"


@dataclass
class TransferRequest:
    """Represents a money transfer request"""
    from_account_number: str
    to_account_number: str
    amount: float
    currency: str
    description: str
    transfer_type: str  # DOMESTIC, INTERNATIONAL
    recipient_bank: Optional[str] = None
    recipient_name: Optional[str] = None

    def validate(self) -> tuple[bool, str]:
        """Validate the transfer request"""
        if self.amount <= 0:
            return False, "Transfer amount must be positive"
        if not self.from_account_number or not self.to_account_number:
            return False, "Both account numbers are required"
        if self.from_account_number == self.to_account_number:
            return False, "Cannot transfer to the same account"
        return True, "Valid"


@dataclass
class BankingSession:
    """Represents an authenticated banking session"""
    session_id: str
    customer_id: str
    login_time: datetime
    last_activity: datetime
    is_active: bool = True

    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired"""
        if not self.is_active:
            return True
        elapsed = datetime.now() - self.last_activity
        return elapsed.total_seconds() > (timeout_minutes * 60)
