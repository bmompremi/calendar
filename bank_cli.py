#!/usr/bin/env python3
"""
Banking Management System - CLI Interface
Interactive command-line interface for managing bank operations.
"""

import sys
from banking_system import Bank, Customer, Account


class BankCLI:
    """Command-line interface for the banking system."""

    def __init__(self):
        self.bank = Bank("Global Banking Corporation")
        self.current_customer = None

    def clear_screen(self):
        """Clear the screen (cross-platform)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the application header."""
        print("=" * 60)
        print(f"  {self.bank.name}".center(60))
        print("  Banking Management System".center(60))
        print("=" * 60)
        print()

    def display_menu(self):
        """Display the main menu."""
        self.display_header()

        if self.current_customer:
            print(f"Logged in as: {self.current_customer.name} ({self.current_customer.customer_id})")
            print()

        print("MAIN MENU:")
        print("1.  Create New Customer")
        print("2.  Login as Customer")
        print("3.  Create New Account")
        print("4.  Deposit Money")
        print("5.  Withdraw Money")
        print("6.  Transfer Money")
        print("7.  Check Balance")
        print("8.  View Transaction History")
        print("9.  View Account Details")
        print("10. View All Accounts")
        print("11. View All Customers")
        print("12. View Bank Summary")
        print("13. Logout")
        print("0.  Exit")
        print()

    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """Get and validate user input."""
        while True:
            try:
                value = input(prompt)

                if not value and not allow_empty:
                    print("Input cannot be empty. Please try again.")
                    continue

                if input_type == float:
                    return float(value)
                elif input_type == int:
                    return int(value)
                else:
                    return value

            except ValueError:
                print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None

    def create_customer(self):
        """Create a new customer."""
        print("\n--- Create New Customer ---")

        name = self.get_input("Enter customer name: ")
        if not name:
            return

        email = self.get_input("Enter email address: ")
        if not email:
            return

        phone = self.get_input("Enter phone number: ")
        if not phone:
            return

        address = self.get_input("Enter address (optional): ", allow_empty=True)

        try:
            customer = self.bank.create_customer(name, email, phone, address)
            print(f"\nCustomer created successfully!")
            print(f"Customer ID: {customer.customer_id}")
            print(f"Name: {customer.name}")
            print(f"\nPlease note your Customer ID for future login.")

        except Exception as e:
            print(f"\nError creating customer: {e}")

        input("\nPress Enter to continue...")

    def login_customer(self):
        """Login as a customer."""
        print("\n--- Customer Login ---")

        customer_id = self.get_input("Enter Customer ID: ")
        if not customer_id:
            return

        customer = self.bank.get_customer(customer_id)
        if customer:
            self.current_customer = customer
            print(f"\nWelcome, {customer.name}!")
        else:
            print("\nCustomer not found. Please check your Customer ID.")

        input("\nPress Enter to continue...")

    def create_account(self):
        """Create a new account."""
        if not self.current_customer:
            print("\nPlease login first to create an account.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Create New Account ---")
        print("Account Types:")
        print("1. Savings")
        print("2. Checking")
        print("3. Business")

        choice = self.get_input("\nSelect account type (1-3): ")

        account_types = {'1': 'savings', '2': 'checking', '3': 'business'}
        account_type = account_types.get(choice)

        if not account_type:
            print("Invalid account type selected.")
            input("\nPress Enter to continue...")
            return

        initial_deposit = self.get_input("Enter initial deposit amount (minimum $0): $", float)
        if initial_deposit is None:
            return

        try:
            account = self.bank.create_account(
                self.current_customer.customer_id,
                account_type,
                initial_deposit
            )
            print(f"\nAccount created successfully!")
            print(f"Account Number: {account.account_number}")
            print(f"Account Type: {account.account_type}")
            print(f"Initial Balance: ${account.balance:.2f}")

        except Exception as e:
            print(f"\nError creating account: {e}")

        input("\nPress Enter to continue...")

    def deposit_money(self):
        """Deposit money into an account."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Deposit Money ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts. Please create an account first.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        choice = self.get_input(f"\nSelect account (1-{len(accounts)}): ", int)
        if choice is None or choice < 1 or choice > len(accounts):
            print("Invalid account selection.")
            input("\nPress Enter to continue...")
            return

        account = accounts[choice - 1]
        amount = self.get_input("Enter deposit amount: $", float)
        if amount is None:
            return

        description = self.get_input("Enter description (optional): ", allow_empty=True)

        try:
            account.deposit(amount, description)
            self.bank.save_data()
            print(f"\nDeposit successful!")
            print(f"Amount Deposited: ${amount:.2f}")
            print(f"New Balance: ${account.balance:.2f}")

        except Exception as e:
            print(f"\nError processing deposit: {e}")

        input("\nPress Enter to continue...")

    def withdraw_money(self):
        """Withdraw money from an account."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Withdraw Money ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        choice = self.get_input(f"\nSelect account (1-{len(accounts)}): ", int)
        if choice is None or choice < 1 or choice > len(accounts):
            print("Invalid account selection.")
            input("\nPress Enter to continue...")
            return

        account = accounts[choice - 1]
        amount = self.get_input("Enter withdrawal amount: $", float)
        if amount is None:
            return

        description = self.get_input("Enter description (optional): ", allow_empty=True)

        try:
            account.withdraw(amount, description)
            self.bank.save_data()
            print(f"\nWithdrawal successful!")
            print(f"Amount Withdrawn: ${amount:.2f}")
            print(f"New Balance: ${account.balance:.2f}")

        except Exception as e:
            print(f"\nError processing withdrawal: {e}")

        input("\nPress Enter to continue...")

    def transfer_money(self):
        """Transfer money between accounts."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Transfer Money ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        from_choice = self.get_input(f"\nSelect source account (1-{len(accounts)}): ", int)
        if from_choice is None or from_choice < 1 or from_choice > len(accounts):
            print("Invalid account selection.")
            input("\nPress Enter to continue...")
            return

        from_account = accounts[from_choice - 1]

        to_account_num = self.get_input("Enter destination account number: ")
        if not to_account_num:
            return

        amount = self.get_input("Enter transfer amount: $", float)
        if amount is None:
            return

        description = self.get_input("Enter description (optional): ", allow_empty=True)

        try:
            self.bank.transfer(from_account.account_number, to_account_num, amount, description)
            print(f"\nTransfer successful!")
            print(f"Amount Transferred: ${amount:.2f}")
            print(f"From: {from_account.account_number}")
            print(f"To: {to_account_num}")
            print(f"New Balance: ${from_account.balance:.2f}")

        except Exception as e:
            print(f"\nError processing transfer: {e}")

        input("\nPress Enter to continue...")

    def check_balance(self):
        """Check account balance."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Check Balance ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. Account: {account.account_number} ({account.account_type})")
            print(f"   Balance: ${account.balance:.2f}")
            print()

        print(f"Total Balance Across All Accounts: ${self.current_customer.get_total_balance():.2f}")

        input("\nPress Enter to continue...")

    def view_transaction_history(self):
        """View transaction history."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Transaction History ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        choice = self.get_input(f"\nSelect account (1-{len(accounts)}): ", int)
        if choice is None or choice < 1 or choice > len(accounts):
            print("Invalid account selection.")
            input("\nPress Enter to continue...")
            return

        account = accounts[choice - 1]
        transactions = account.get_transaction_history()

        if not transactions:
            print("\nNo transactions found for this account.")
        else:
            print(f"\nTransaction History for Account {account.account_number}:")
            print("-" * 80)
            for trans in transactions:
                print(trans)
            print("-" * 80)
            print(f"Total Transactions: {len(transactions)}")

        input("\nPress Enter to continue...")

    def view_account_details(self):
        """View detailed account information."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Account Details ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
            input("\nPress Enter to continue...")
            return

        print("\nYour Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        choice = self.get_input(f"\nSelect account (1-{len(accounts)}): ", int)
        if choice is None or choice < 1 or choice > len(accounts):
            print("Invalid account selection.")
            input("\nPress Enter to continue...")
            return

        account = accounts[choice - 1]

        print(f"\n{'=' * 60}")
        print(f"Account Details")
        print(f"{'=' * 60}")
        print(f"Account Number: {account.account_number}")
        print(f"Account Type: {account.account_type}")
        print(f"Balance: ${account.balance:.2f}")
        print(f"Status: {'Active' if account.is_active else 'Inactive'}")
        print(f"Created: {account.created_at}")
        print(f"Total Transactions: {len(account.transactions)}")
        print(f"{'=' * 60}")

        input("\nPress Enter to continue...")

    def view_all_accounts(self):
        """View all accounts for current customer."""
        if not self.current_customer:
            print("\nPlease login first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- All Your Accounts ---")

        accounts = self.current_customer.get_all_accounts()
        if not accounts:
            print("You don't have any accounts.")
        else:
            for account in accounts:
                print(f"\n{account}")
                print(f"  Created: {account.created_at}")
                print(f"  Transactions: {len(account.transactions)}")

        input("\nPress Enter to continue...")

    def view_all_customers(self):
        """View all customers (admin feature)."""
        print("\n--- All Customers ---")

        customers = self.bank.list_all_customers()
        if not customers:
            print("No customers found.")
        else:
            for i, customer in enumerate(customers, 1):
                print(f"\n{i}. {customer}")
                print(f"   Total Balance: ${customer.get_total_balance():.2f}")
                print(f"   Number of Accounts: {len(customer.get_all_accounts())}")

        input("\nPress Enter to continue...")

    def view_bank_summary(self):
        """View bank summary statistics."""
        print("\n--- Bank Summary ---")

        summary = self.bank.get_bank_summary()

        print(f"\nBank Name: {self.bank.name}")
        print(f"Total Customers: {summary['total_customers']}")
        print(f"Total Accounts: {summary['total_accounts']}")
        print(f"Total Deposits: ${summary['total_deposits']:.2f}")

        input("\nPress Enter to continue...")

    def logout(self):
        """Logout current customer."""
        if self.current_customer:
            print(f"\nLogging out {self.current_customer.name}...")
            self.current_customer = None
            print("Logged out successfully.")
        else:
            print("\nNo customer is currently logged in.")

        input("\nPress Enter to continue...")

    def run(self):
        """Run the main application loop."""
        while True:
            self.clear_screen()
            self.display_menu()

            choice = self.get_input("Enter your choice: ")

            if choice == '1':
                self.create_customer()
            elif choice == '2':
                self.login_customer()
            elif choice == '3':
                self.create_account()
            elif choice == '4':
                self.deposit_money()
            elif choice == '5':
                self.withdraw_money()
            elif choice == '6':
                self.transfer_money()
            elif choice == '7':
                self.check_balance()
            elif choice == '8':
                self.view_transaction_history()
            elif choice == '9':
                self.view_account_details()
            elif choice == '10':
                self.view_all_accounts()
            elif choice == '11':
                self.view_all_customers()
            elif choice == '12':
                self.view_bank_summary()
            elif choice == '13':
                self.logout()
            elif choice == '0':
                print("\nThank you for using Global Banking Corporation!")
                print("Goodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    try:
        cli = BankCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
