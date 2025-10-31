"""
Banking Management System
A comprehensive banking application with account management, transactions, and data persistence.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class Transaction:
    """Represents a single transaction in the banking system."""

    def __init__(self, transaction_type: str, amount: float, from_account: str = None,
                 to_account: str = None, description: str = ""):
        self.id = str(uuid.uuid4())
        self.transaction_type = transaction_type  # 'deposit', 'withdrawal', 'transfer'
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.description = description
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'type': self.transaction_type,
            'amount': self.amount,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'description': self.description,
            'timestamp': self.timestamp
        }

    def __str__(self) -> str:
        """String representation of transaction."""
        return (f"[{self.timestamp}] {self.transaction_type.upper()}: "
                f"${self.amount:.2f} - {self.description}")


class Account:
    """Represents a bank account."""

    def __init__(self, account_number: str, account_type: str, balance: float = 0.0):
        self.account_number = account_number
        self.account_type = account_type  # 'savings', 'checking', 'business'
        self.balance = balance
        self.transactions: List[Transaction] = []
        self.created_at = datetime.now().isoformat()
        self.is_active = True

    def deposit(self, amount: float, description: str = "") -> bool:
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        transaction = Transaction('deposit', amount, to_account=self.account_number,
                                 description=description)
        self.transactions.append(transaction)
        return True

    def withdraw(self, amount: float, description: str = "") -> bool:
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Available balance: ${self.balance:.2f}")

        self.balance -= amount
        transaction = Transaction('withdrawal', amount, from_account=self.account_number,
                                 description=description)
        self.transactions.append(transaction)
        return True

    def get_balance(self) -> float:
        """Get current account balance."""
        return self.balance

    def get_transaction_history(self, limit: int = None) -> List[Transaction]:
        """Get transaction history."""
        if limit:
            return self.transactions[-limit:]
        return self.transactions

    def to_dict(self) -> Dict:
        """Convert account to dictionary."""
        return {
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'transactions': [t.to_dict() for t in self.transactions],
            'created_at': self.created_at,
            'is_active': self.is_active
        }

    def __str__(self) -> str:
        """String representation of account."""
        status = "Active" if self.is_active else "Inactive"
        return (f"Account #{self.account_number} ({self.account_type}) - "
                f"Balance: ${self.balance:.2f} - Status: {status}")


class Customer:
    """Represents a bank customer."""

    def __init__(self, customer_id: str, name: str, email: str, phone: str, address: str = ""):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.accounts: Dict[str, Account] = {}
        self.created_at = datetime.now().isoformat()

    def add_account(self, account: Account) -> None:
        """Add an account to the customer."""
        self.accounts[account.account_number] = account

    def get_account(self, account_number: str) -> Optional[Account]:
        """Get a specific account."""
        return self.accounts.get(account_number)

    def get_all_accounts(self) -> List[Account]:
        """Get all customer accounts."""
        return list(self.accounts.values())

    def get_total_balance(self) -> float:
        """Get total balance across all accounts."""
        return sum(account.balance for account in self.accounts.values())

    def to_dict(self) -> Dict:
        """Convert customer to dictionary."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'accounts': {num: acc.to_dict() for num, acc in self.accounts.items()},
            'created_at': self.created_at
        }

    def __str__(self) -> str:
        """String representation of customer."""
        return (f"Customer #{self.customer_id}: {self.name} - "
                f"Email: {self.email} - Accounts: {len(self.accounts)}")


class Bank:
    """Main bank management system."""

    def __init__(self, name: str = "Python Bank", data_file: str = "bank_data.json"):
        self.name = name
        self.customers: Dict[str, Customer] = {}
        self.data_file = data_file
        self.account_counter = 1000
        self.customer_counter = 1000
        self.load_data()

    def generate_account_number(self) -> str:
        """Generate a unique account number."""
        self.account_counter += 1
        return f"ACC{self.account_counter:08d}"

    def generate_customer_id(self) -> str:
        """Generate a unique customer ID."""
        self.customer_counter += 1
        return f"CUST{self.customer_counter:08d}"

    def create_customer(self, name: str, email: str, phone: str, address: str = "") -> Customer:
        """Create a new customer."""
        customer_id = self.generate_customer_id()
        customer = Customer(customer_id, name, email, phone, address)
        self.customers[customer_id] = customer
        self.save_data()
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        return self.customers.get(customer_id)

    def create_account(self, customer_id: str, account_type: str, initial_deposit: float = 0.0) -> Account:
        """Create a new account for a customer."""
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        if account_type not in ['savings', 'checking', 'business']:
            raise ValueError("Invalid account type. Must be 'savings', 'checking', or 'business'")

        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")

        account_number = self.generate_account_number()
        account = Account(account_number, account_type, initial_deposit)

        if initial_deposit > 0:
            account.deposit(initial_deposit, "Initial deposit")
            account.balance = initial_deposit  # Reset balance after deposit to avoid double counting

        customer.add_account(account)
        self.save_data()
        return account

    def transfer(self, from_account_num: str, to_account_num: str, amount: float, description: str = "") -> bool:
        """Transfer money between accounts."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        # Find the accounts
        from_account = None
        to_account = None

        for customer in self.customers.values():
            if from_account_num in customer.accounts:
                from_account = customer.accounts[from_account_num]
            if to_account_num in customer.accounts:
                to_account = customer.accounts[to_account_num]

        if not from_account:
            raise ValueError(f"Source account {from_account_num} not found")
        if not to_account:
            raise ValueError(f"Destination account {to_account_num} not found")

        # Perform transfer
        from_account.withdraw(amount, f"Transfer to {to_account_num}: {description}")
        to_account.deposit(amount, f"Transfer from {from_account_num}: {description}")

        # Create transfer transaction record
        transfer_transaction = Transaction('transfer', amount, from_account_num,
                                          to_account_num, description)

        self.save_data()
        return True

    def get_account(self, account_number: str) -> Optional[Account]:
        """Find an account by account number."""
        for customer in self.customers.values():
            if account_number in customer.accounts:
                return customer.accounts[account_number]
        return None

    def list_all_customers(self) -> List[Customer]:
        """Get all customers."""
        return list(self.customers.values())

    def save_data(self) -> None:
        """Save bank data to JSON file."""
        data = {
            'name': self.name,
            'account_counter': self.account_counter,
            'customer_counter': self.customer_counter,
            'customers': {cid: customer.to_dict() for cid, customer in self.customers.items()}
        }

        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self) -> None:
        """Load bank data from JSON file."""
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

            self.name = data.get('name', self.name)
            self.account_counter = data.get('account_counter', 1000)
            self.customer_counter = data.get('customer_counter', 1000)

            # Load customers
            for cid, cust_data in data.get('customers', {}).items():
                customer = Customer(
                    cust_data['customer_id'],
                    cust_data['name'],
                    cust_data['email'],
                    cust_data['phone'],
                    cust_data.get('address', '')
                )
                customer.created_at = cust_data['created_at']

                # Load accounts
                for acc_num, acc_data in cust_data['accounts'].items():
                    account = Account(
                        acc_data['account_number'],
                        acc_data['account_type'],
                        acc_data['balance']
                    )
                    account.created_at = acc_data['created_at']
                    account.is_active = acc_data['is_active']

                    # Load transactions
                    for trans_data in acc_data['transactions']:
                        trans = Transaction(
                            trans_data['type'],
                            trans_data['amount'],
                            trans_data.get('from_account'),
                            trans_data.get('to_account'),
                            trans_data.get('description', '')
                        )
                        trans.id = trans_data['id']
                        trans.timestamp = trans_data['timestamp']
                        account.transactions.append(trans)

                    customer.add_account(account)

                self.customers[cid] = customer

        except Exception as e:
            print(f"Error loading data: {e}")
            print("Starting with empty bank database.")

    def get_bank_summary(self) -> Dict:
        """Get summary of bank statistics."""
        total_customers = len(self.customers)
        total_accounts = sum(len(customer.accounts) for customer in self.customers.values())
        total_deposits = sum(customer.get_total_balance() for customer in self.customers.values())

        return {
            'total_customers': total_customers,
            'total_accounts': total_accounts,
            'total_deposits': total_deposits
        }

    def __str__(self) -> str:
        """String representation of bank."""
        summary = self.get_bank_summary()
        return (f"{self.name} - Customers: {summary['total_customers']}, "
                f"Accounts: {summary['total_accounts']}, "
                f"Total Deposits: ${summary['total_deposits']:.2f}")
