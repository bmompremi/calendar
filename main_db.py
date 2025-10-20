#!/usr/bin/env python3
"""
Haiti Banking Management System - Main CLI Interface with Neon Postgres
A comprehensive banking system with money transfer capabilities for Haiti
"""

from datetime import datetime
from banking_system_db import BankingSystemDB
from transfer_system_db import TransferSystemDB
from models import TransferRequest
from config import HAITI_BANKS, ACCOUNT_TYPES, DEFAULT_CURRENCY
import sys
import os


class BankingCLI:
    """Command-line interface for the banking system with database"""

    def __init__(self, connection_string: str = None):
        try:
            self.banking_system = BankingSystemDB(connection_string)
            self.transfer_system = TransferSystemDB(self.banking_system)
            self.current_session = None
            self.current_customer = None
        except ValueError as e:
            print(f"\n❌ Error: {e}")
            print("\nPlease ensure:")
            print("1. You have created a .env file with DATABASE_URL")
            print("2. You have run 'python init_db.py' to initialize the database")
            print("3. Your Neon database is accessible")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Database connection error: {e}")
            sys.exit(1)

    def __del__(self):
        """Cleanup database connections"""
        if hasattr(self, 'banking_system'):
            self.banking_system.close()

    def print_header(self):
        """Print application header"""
        print("\n" + "=" * 60)
        print(" " * 10 + "HAITI BANKING MANAGEMENT SYSTEM")
        print(" " * 15 + "Sistèm Bankè Ayiti")
        print(" " * 13 + "(Powered by Neon Postgres)")
        print("=" * 60)

    def print_menu(self):
        """Print main menu"""
        print("\n--- MAIN MENU ---")
        if self.current_customer:
            print(f"Logged in as: {self.current_customer.get_full_name()}")
            print("\n1. View My Accounts")
            print("2. Create New Account")
            print("3. Deposit Money")
            print("4. Withdraw Money")
            print("5. Transfer Money (Domestic)")
            print("6. Transfer Money (International)")
            print("7. View Transaction History")
            print("8. View Account Statement")
            print("9. Check Daily Transfer Limits")
            print("10. Logout")
        else:
            print("1. Register New Customer")
            print("2. Login")
            print("3. Exit")

    def register_customer(self):
        """Register a new customer"""
        print("\n--- CUSTOMER REGISTRATION ---")
        try:
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            address = input("Address: ").strip()
            city = input("City: ").strip()
            country = input("Country (default: Haiti): ").strip() or "Haiti"
            dob_str = input("Date of Birth (YYYY-MM-DD): ").strip()
            national_id = input("National ID: ").strip()
            password = input("Password: ").strip()

            # Parse date of birth
            dob = datetime.strptime(dob_str, "%Y-%m-%d")

            # Create customer
            customer = self.banking_system.create_customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                country=country,
                date_of_birth=dob,
                national_id=national_id,
                password=password
            )

            print(f"\n✅ Customer registered successfully!")
            print(f"Customer ID: {customer.customer_id}")
            print(f"Email: {customer.email}")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

    def login(self):
        """Login a customer"""
        print("\n--- LOGIN ---")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        try:
            customer = self.banking_system.authenticate_customer(email, password)
            if customer:
                self.current_customer = customer
                self.current_session = self.banking_system.create_session(customer.customer_id)
                print(f"\n✅ Welcome back, {customer.get_full_name()}!")
            else:
                print("\n❌ Invalid credentials. Please try again.")
        except Exception as e:
            print(f"\n❌ Login error: {e}")

    def logout(self):
        """Logout current customer"""
        if self.current_session:
            self.banking_system.end_session(self.current_session.session_id)
        self.current_customer = None
        self.current_session = None
        print("\n✅ Logged out successfully.")

    def create_account(self):
        """Create a new bank account"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- CREATE NEW ACCOUNT ---")
        print("Account Types:", ", ".join(ACCOUNT_TYPES))
        account_type = input("Account Type: ").strip().upper()

        if account_type not in ACCOUNT_TYPES:
            print(f"❌ Invalid account type. Must be one of: {ACCOUNT_TYPES}")
            return

        currency = input(f"Currency (default: {DEFAULT_CURRENCY}): ").strip().upper() or DEFAULT_CURRENCY
        initial_deposit_str = input("Initial Deposit (0 if none): ").strip()

        try:
            initial_deposit = float(initial_deposit_str)
            account = self.banking_system.create_account(
                customer_id=self.current_customer.customer_id,
                account_type=account_type,
                initial_deposit=initial_deposit,
                currency=currency
            )

            print(f"\n✅ Account created successfully!")
            print(f"Account Number: {account.account_number}")
            print(f"Type: {account.account_type}")
            print(f"Balance: {account.currency} {account.balance:,.2f}")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

    def view_accounts(self):
        """View all accounts for current customer"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        try:
            accounts = self.banking_system.get_customer_accounts(self.current_customer.customer_id)

            if not accounts:
                print("\n⚠️  You don't have any accounts yet.")
                return

            print("\n--- YOUR ACCOUNTS ---")
            for i, account in enumerate(accounts, 1):
                print(f"\n{i}. Account Number: {account.account_number}")
                print(f"   Type: {account.account_type}")
                print(f"   Balance: {account.currency} {account.balance:,.2f}")
                print(f"   Status: {account.status}")
                print(f"   Created: {account.created_at.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def deposit_money(self):
        """Deposit money into an account"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- DEPOSIT MONEY ---")
        account_number = input("Account Number: ").strip()
        amount_str = input("Amount: ").strip()

        try:
            amount = float(amount_str)
            success, message, transaction = self.banking_system.deposit(account_number, amount)

            if success:
                print(f"\n✅ {message}")
                if transaction:
                    print(f"Transaction Reference: {transaction.reference_number}")
                    print(f"Timestamp: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n❌ {message}")

        except ValueError:
            print(f"\n❌ Error: Invalid amount")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def withdraw_money(self):
        """Withdraw money from an account"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- WITHDRAW MONEY ---")
        account_number = input("Account Number: ").strip()
        amount_str = input("Amount: ").strip()

        try:
            amount = float(amount_str)
            success, message, transaction = self.banking_system.withdraw(account_number, amount)

            if success:
                print(f"\n✅ {message}")
                if transaction:
                    print(f"Transaction Reference: {transaction.reference_number}")
                    print(f"Timestamp: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n❌ {message}")

        except ValueError:
            print(f"\n❌ Error: Invalid amount")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def transfer_domestic(self):
        """Transfer money domestically"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- DOMESTIC MONEY TRANSFER ---")
        from_account = input("From Account Number: ").strip()
        to_account = input("To Account Number: ").strip()
        amount_str = input("Amount (HTG): ").strip()
        description = input("Description (optional): ").strip() or "Domestic transfer"

        try:
            amount = float(amount_str)
            success, message, transaction = self.transfer_system.transfer_domestic(
                from_account, to_account, amount, description
            )

            if success:
                print(f"\n✅ {message}")
                if transaction:
                    print(f"Transaction Reference: {transaction.reference_number}")
                    print(f"Timestamp: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n❌ {message}")

        except ValueError:
            print(f"\n❌ Error: Invalid amount")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def transfer_international(self):
        """Transfer money internationally"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- INTERNATIONAL MONEY TRANSFER ---")
        from_account = input("From Account Number: ").strip()
        recipient_name = input("Recipient Name: ").strip()
        recipient_bank = input("Recipient Bank: ").strip()
        recipient_account = input("Recipient Account Number: ").strip()
        amount_str = input("Amount (HTG): ").strip()
        currency = input("Target Currency (USD/HTG): ").strip().upper() or "USD"
        description = input("Description (optional): ").strip() or "International transfer"

        try:
            amount = float(amount_str)
            success, message, transaction = self.transfer_system.transfer_international(
                from_account, recipient_name, recipient_bank, recipient_account,
                amount, currency, description
            )

            if success:
                print(f"\n✅ {message}")
                if transaction:
                    print(f"Transaction Reference: {transaction.reference_number}")
                    print(f"Timestamp: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n❌ {message}")

        except ValueError:
            print(f"\n❌ Error: Invalid amount")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def view_transaction_history(self):
        """View transaction history"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- TRANSACTION HISTORY ---")
        account_number = input("Account Number: ").strip()
        limit_str = input("Number of transactions (default: 10): ").strip() or "10"

        try:
            limit = int(limit_str)
            transactions = self.banking_system.get_account_transactions(account_number, limit)

            if not transactions:
                print("\n⚠️  No transactions found.")
                return

            print(f"\nShowing last {len(transactions)} transactions:")
            for i, txn in enumerate(transactions, 1):
                print(f"\n{i}. {txn.reference_number}")
                print(f"   Type: {txn.transaction_type}")
                print(f"   Amount: {txn.currency} {txn.amount:,.2f}")
                if txn.fee > 0:
                    print(f"   Fee: {txn.fee:,.2f}")
                print(f"   Status: {txn.status}")
                print(f"   Date: {txn.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Description: {txn.description}")

        except ValueError:
            print(f"\n❌ Error: Invalid limit")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def view_account_statement(self):
        """View account statement"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- ACCOUNT STATEMENT ---")
        account_number = input("Account Number: ").strip()
        days_str = input("Number of days (default: 30): ").strip() or "30"

        try:
            days = int(days_str)
            from datetime import timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            transactions = self.banking_system.get_account_statement(
                account_number, start_date, end_date
            )

            account = self.banking_system.get_account(account_number)
            if not account:
                print("\n❌ Account not found.")
                return

            print(f"\n--- Account Statement for {account_number} ---")
            print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            print(f"Current Balance: {account.currency} {account.balance:,.2f}")
            print(f"\nTransactions: {len(transactions)}")

            for txn in transactions:
                print(f"\n{txn.timestamp.strftime('%Y-%m-%d %H:%M')} | {txn.transaction_type}")
                print(f"  {txn.currency} {txn.amount:,.2f} | {txn.description}")
                if txn.fee > 0:
                    print(f"  Fee: {txn.fee:,.2f}")

        except ValueError:
            print(f"\n❌ Error: Invalid number of days")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def check_transfer_limits(self):
        """Check daily transfer limits"""
        if not self.current_customer:
            print("\n❌ Please login first.")
            return

        print("\n--- DAILY TRANSFER LIMITS ---")
        account_number = input("Account Number: ").strip()

        try:
            summary = self.transfer_system.get_daily_transfer_summary(account_number)

            if "error" in summary:
                print(f"\n❌ {summary['error']}")
                return

            print(f"\nAccount: {summary['account_number']}")
            print(f"Daily Limit: HTG {summary['daily_limit']:,.2f}")
            print(f"Used Today: HTG {summary['daily_total']:,.2f}")
            print(f"Remaining: HTG {summary['remaining_limit']:,.2f}")
            if summary['last_transfer_date']:
                print(f"Last Transfer: {summary['last_transfer_date'].strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

    def run(self):
        """Run the CLI application"""
        self.print_header()
        print("\n🌟 Welcome to Haiti Banking Management System")
        print("   Byenveni nan Sistèm Jesyon Bankè Ayiti")
        print("\n🚀 Connected to Neon Postgres Database")

        while True:
            self.print_menu()
            choice = input("\nEnter your choice: ").strip()

            if not self.current_customer:
                # Not logged in
                if choice == "1":
                    self.register_customer()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    print("\n👋 Thank you for using Haiti Banking System. Goodbye!")
                    print("   Mèsi pou itilize Sistèm Bankè Ayiti. Orevwa!")
                    self.banking_system.close()
                    sys.exit(0)
                else:
                    print("\n❌ Invalid choice. Please try again.")
            else:
                # Logged in
                if choice == "1":
                    self.view_accounts()
                elif choice == "2":
                    self.create_account()
                elif choice == "3":
                    self.deposit_money()
                elif choice == "4":
                    self.withdraw_money()
                elif choice == "5":
                    self.transfer_domestic()
                elif choice == "6":
                    self.transfer_international()
                elif choice == "7":
                    self.view_transaction_history()
                elif choice == "8":
                    self.view_account_statement()
                elif choice == "9":
                    self.check_transfer_limits()
                elif choice == "10":
                    self.logout()
                else:
                    print("\n❌ Invalid choice. Please try again.")


def main():
    """Main entry point"""
    cli = BankingCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
