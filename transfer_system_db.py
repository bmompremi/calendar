"""
Money Transfer System for Haiti Banking with Neon Postgres Database
Handles domestic and international transfers
"""

from datetime import datetime, timedelta
from typing import Optional, List
from models import Account, Transaction, TransferRequest
from config import (
    MAX_DAILY_TRANSFER_LIMIT, MAX_SINGLE_TRANSFER_LIMIT,
    MIN_TRANSFER_AMOUNT, EXCHANGE_RATES
)


class TransferSystemDB:
    """Handles money transfers between accounts with database persistence"""

    def __init__(self, banking_system):
        self.banking_system = banking_system
        self.transfer_fees = {
            'DOMESTIC': 0.01,  # 1% for domestic transfers
            'INTERNATIONAL': 0.025,  # 2.5% for international transfers
        }
        self.min_fee = 5.0  # HTG
        self.max_fee = 500.0  # HTG

    def calculate_transfer_fee(self, amount: float, transfer_type: str) -> float:
        """Calculate transfer fee based on amount and type"""
        fee_rate = self.transfer_fees.get(transfer_type, 0.01)
        fee = amount * fee_rate

        # Apply min/max fee limits
        fee = max(self.min_fee, min(fee, self.max_fee))
        return round(fee, 2)

    def check_daily_limit(self, account_number: str, amount: float) -> tuple[bool, str]:
        """Check if transfer amount is within daily limits"""
        account = self.banking_system.get_account(account_number)
        if not account:
            return False, "Account not found"

        # Reset daily total if it's a new day
        today = datetime.now().date()
        if account.last_transfer_date:
            last_transfer_date = account.last_transfer_date.date()
            if last_transfer_date < today:
                # Reset in database
                self.banking_system.db_manager.reset_daily_transfer_total(account_number)
                account.daily_transfer_total = 0.0
                account.last_transfer_date = None

        # Check single transfer limit
        if amount > MAX_SINGLE_TRANSFER_LIMIT:
            return False, f"Transfer amount exceeds single transfer limit of {MAX_SINGLE_TRANSFER_LIMIT:,.2f} HTG"

        # Check daily limit
        potential_total = account.daily_transfer_total + amount
        if potential_total > MAX_DAILY_TRANSFER_LIMIT:
            remaining = MAX_DAILY_TRANSFER_LIMIT - account.daily_transfer_total
            return False, f"Transfer would exceed daily limit. Remaining limit: {remaining:,.2f} HTG"

        return True, "Within limits"

    def transfer_domestic(self, from_account_number: str, to_account_number: str,
                         amount: float, description: str = "Domestic transfer") -> tuple[bool, str, Optional[Transaction]]:
        """Transfer money between accounts in the same bank (domestic)"""

        # Validate inputs
        if amount < MIN_TRANSFER_AMOUNT:
            return False, f"Minimum transfer amount is {MIN_TRANSFER_AMOUNT} HTG", None

        if from_account_number == to_account_number:
            return False, "Cannot transfer to the same account", None

        # Get accounts
        from_account = self.banking_system.get_account(from_account_number)
        to_account = self.banking_system.get_account(to_account_number)

        if not from_account:
            return False, "Source account not found", None
        if not to_account:
            return False, "Destination account not found", None

        # Check account status
        if from_account.status != "ACTIVE":
            return False, f"Source account is {from_account.status}", None
        if to_account.status != "ACTIVE":
            return False, f"Destination account is {to_account.status}", None

        # Check daily limits
        limit_ok, limit_msg = self.check_daily_limit(from_account_number, amount)
        if not limit_ok:
            return False, limit_msg, None

        # Calculate fee
        fee = self.calculate_transfer_fee(amount, 'DOMESTIC')
        total_debit = amount + fee

        # Check balance
        if from_account.balance < total_debit:
            return False, f"Insufficient funds. Need {total_debit:,.2f} HTG (amount + fee)", None

        # Handle currency conversion if needed
        exchange_rate = 1.0
        recipient_amount = amount

        if from_account.currency != to_account.currency:
            # Convert from source currency to destination currency
            from_rate = EXCHANGE_RATES.get(from_account.currency, 1.0)
            to_rate = EXCHANGE_RATES.get(to_account.currency, 1.0)
            exchange_rate = to_rate / from_rate
            recipient_amount = amount * exchange_rate

        # Perform transfer - update balances in database
        new_from_balance = from_account.balance - total_debit
        new_to_balance = to_account.balance + recipient_amount

        self.banking_system.db_manager.update_account_balance(from_account_number, new_from_balance)
        self.banking_system.db_manager.update_account_balance(to_account_number, new_to_balance)

        # Update daily transfer tracking
        timestamp = datetime.now()
        self.banking_system.db_manager.update_daily_transfer_total(
            from_account_number, amount, timestamp
        )

        # Record transactions
        # Debit transaction
        debit_txn = self.banking_system._record_transaction(
            from_account=from_account_number,
            to_account=to_account_number,
            amount=amount,
            currency=from_account.currency,
            transaction_type="TRANSFER_SENT",
            description=description,
            fee=fee,
            exchange_rate=exchange_rate
        )

        # Credit transaction
        self.banking_system._record_transaction(
            from_account=from_account_number,
            to_account=to_account_number,
            amount=recipient_amount,
            currency=to_account.currency,
            transaction_type="TRANSFER_RECEIVED",
            description=description,
            fee=0.0,
            exchange_rate=exchange_rate
        )

        success_msg = f"Successfully transferred {from_account.currency} {amount:,.2f} to account {to_account_number}. Fee: {fee:,.2f} HTG"
        return True, success_msg, debit_txn

    def transfer_international(self, from_account_number: str,
                              recipient_name: str, recipient_bank: str,
                              recipient_account: str, amount: float,
                              currency: str = "USD",
                              description: str = "International transfer") -> tuple[bool, str, Optional[Transaction]]:
        """Transfer money to an international account"""

        # Validate inputs
        if amount < MIN_TRANSFER_AMOUNT:
            return False, f"Minimum transfer amount is {MIN_TRANSFER_AMOUNT} HTG", None

        # Get source account
        from_account = self.banking_system.get_account(from_account_number)
        if not from_account:
            return False, "Source account not found", None

        if from_account.status != "ACTIVE":
            return False, f"Source account is {from_account.status}", None

        # Check daily limits
        limit_ok, limit_msg = self.check_daily_limit(from_account_number, amount)
        if not limit_ok:
            return False, limit_msg, None

        # Calculate fee (higher for international)
        fee = self.calculate_transfer_fee(amount, 'INTERNATIONAL')
        total_debit = amount + fee

        # Check balance
        if from_account.balance < total_debit:
            return False, f"Insufficient funds. Need {total_debit:,.2f} HTG (amount + fee)", None

        # Convert to target currency
        from_rate = EXCHANGE_RATES.get(from_account.currency, 1.0)
        to_rate = EXCHANGE_RATES.get(currency, 1.0)
        exchange_rate = to_rate / from_rate
        converted_amount = amount * exchange_rate

        # Perform transfer - update balance in database
        new_balance = from_account.balance - total_debit
        self.banking_system.db_manager.update_account_balance(from_account_number, new_balance)

        # Update daily transfer tracking
        timestamp = datetime.now()
        self.banking_system.db_manager.update_daily_transfer_total(
            from_account_number, amount, timestamp
        )

        # Record transaction
        transaction = self.banking_system._record_transaction(
            from_account=from_account_number,
            to_account=f"{recipient_bank}:{recipient_account}",
            amount=amount,
            currency=from_account.currency,
            transaction_type="TRANSFER_INTERNATIONAL",
            description=f"{description} to {recipient_name} at {recipient_bank}",
            fee=fee,
            exchange_rate=exchange_rate
        )

        success_msg = (
            f"Successfully sent {from_account.currency} {amount:,.2f} "
            f"(~{currency} {converted_amount:,.2f}) to {recipient_name}. "
            f"Fee: {fee:,.2f} HTG"
        )
        return True, success_msg, transaction

    def get_transfer_history(self, account_number: str, days: int = 30) -> List[Transaction]:
        """Get transfer history for an account"""
        cutoff_date = datetime.now() - timedelta(days=days)
        transactions = self.banking_system.db_manager.get_transfer_history(
            account_number, cutoff_date
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
            for txn in transactions
        ]

    def get_daily_transfer_summary(self, account_number: str) -> dict:
        """Get summary of today's transfers"""
        account = self.banking_system.get_account(account_number)
        if not account:
            return {"error": "Account not found"}

        return {
            "account_number": account_number,
            "daily_total": account.daily_transfer_total,
            "daily_limit": MAX_DAILY_TRANSFER_LIMIT,
            "remaining_limit": MAX_DAILY_TRANSFER_LIMIT - account.daily_transfer_total,
            "last_transfer_date": account.last_transfer_date
        }

    def request_transfer(self, request: TransferRequest) -> tuple[bool, str, Optional[Transaction]]:
        """Process a transfer request"""
        # Validate request
        is_valid, msg = request.validate()
        if not is_valid:
            return False, msg, None

        # Route to appropriate transfer method
        if request.transfer_type == "DOMESTIC":
            return self.transfer_domestic(
                request.from_account_number,
                request.to_account_number,
                request.amount,
                request.description
            )
        elif request.transfer_type == "INTERNATIONAL":
            return self.transfer_international(
                request.from_account_number,
                request.recipient_name,
                request.recipient_bank,
                request.to_account_number,
                request.amount,
                request.currency,
                request.description
            )
        else:
            return False, f"Invalid transfer type: {request.transfer_type}", None
