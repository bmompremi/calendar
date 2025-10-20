#!/usr/bin/env python3
"""
Demo script for Haiti Banking Management System with Neon Postgres
Demonstrates all features of the banking system with database persistence
"""

from datetime import datetime
from banking_system_db import BankingSystemDB
from transfer_system_db import TransferSystemDB
import sys


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo():
    """Run the demo"""
    print_section("HAITI BANKING SYSTEM WITH NEON POSTGRES - DEMO")

    # Initialize the system with database
    try:
        print("\n🔌 Connecting to Neon Postgres database...")
        banking_system = BankingSystemDB()
        transfer_system = TransferSystemDB(banking_system)
        print("✅ Connected successfully!")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. You have created a .env file with DATABASE_URL")
        print("2. You have run 'python init_db.py' to initialize the database")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Database connection error: {e}")
        sys.exit(1)

    try:
        # 1. Create customers
        print_section("1. CREATING CUSTOMERS")

        customer1 = banking_system.create_customer(
            first_name="Jean",
            last_name="Baptiste",
            email=f"jean.baptiste.{datetime.now().timestamp()}@example.ht",  # Unique email
            phone="+509-1234-5678",
            address="123 Rue de la République",
            city="Port-au-Prince",
            country="Haiti",
            date_of_birth=datetime(1985, 3, 15),
            national_id=f"NIF-{int(datetime.now().timestamp())}",  # Unique ID
            password="secure_password123"
        )
        print(f"✅ Created customer: {customer1.get_full_name()}")
        print(f"   Email: {customer1.email}")
        print(f"   Customer ID: {customer1.customer_id}")

        customer2 = banking_system.create_customer(
            first_name="Marie",
            last_name="Duval",
            email=f"marie.duval.{datetime.now().timestamp()}@example.ht",  # Unique email
            phone="+509-9876-5432",
            address="456 Avenue John Brown",
            city="Cap-Haïtien",
            country="Haiti",
            date_of_birth=datetime(1990, 7, 22),
            national_id=f"NIF-{int(datetime.now().timestamp()) + 1}",  # Unique ID
            password="another_secure_pass"
        )
        print(f"\n✅ Created customer: {customer2.get_full_name()}")
        print(f"   Email: {customer2.email}")
        print(f"   Customer ID: {customer2.customer_id}")

        # 2. Create accounts
        print_section("2. CREATING BANK ACCOUNTS")

        account1 = banking_system.create_account(
            customer_id=customer1.customer_id,
            account_type="CHECKING",
            initial_deposit=50000.00,
            currency="HTG"
        )
        print(f"✅ Created checking account for {customer1.get_full_name()}")
        print(f"   Account Number: {account1.account_number}")
        print(f"   Balance: {account1.currency} {account1.balance:,.2f}")

        account2 = banking_system.create_account(
            customer_id=customer1.customer_id,
            account_type="SAVINGS",
            initial_deposit=100000.00,
            currency="HTG"
        )
        print(f"\n✅ Created savings account for {customer1.get_full_name()}")
        print(f"   Account Number: {account2.account_number}")
        print(f"   Balance: {account2.currency} {account2.balance:,.2f}")

        account3 = banking_system.create_account(
            customer_id=customer2.customer_id,
            account_type="CHECKING",
            initial_deposit=75000.00,
            currency="HTG"
        )
        print(f"\n✅ Created checking account for {customer2.get_full_name()}")
        print(f"   Account Number: {account3.account_number}")
        print(f"   Balance: {account3.currency} {account3.balance:,.2f}")

        # 3. Deposit money
        print_section("3. DEPOSITING MONEY")

        success, msg, txn = banking_system.deposit(account1.account_number, 25000.00, "Salary deposit")
        print(f"✅ Deposit to account {account1.account_number}:")
        print(f"   {msg}")
        # Refresh account
        account1 = banking_system.get_account(account1.account_number)
        print(f"   New Balance: HTG {account1.balance:,.2f}")
        print(f"   Transaction Ref: {txn.reference_number}")

        # 4. Withdraw money
        print_section("4. WITHDRAWING MONEY")

        success, msg, txn = banking_system.withdraw(account1.account_number, 10000.00, "ATM withdrawal")
        print(f"✅ Withdrawal from account {account1.account_number}:")
        print(f"   {msg}")
        # Refresh account
        account1 = banking_system.get_account(account1.account_number)
        print(f"   New Balance: HTG {account1.balance:,.2f}")
        print(f"   Transaction Ref: {txn.reference_number}")

        # 5. Domestic transfer
        print_section("5. DOMESTIC MONEY TRANSFER")

        # Refresh accounts to get current balances
        account1 = banking_system.get_account(account1.account_number)
        account3 = banking_system.get_account(account3.account_number)

        print(f"Before transfer:")
        print(f"  Account {account1.account_number} balance: HTG {account1.balance:,.2f}")
        print(f"  Account {account3.account_number} balance: HTG {account3.balance:,.2f}")

        success, msg, txn = transfer_system.transfer_domestic(
            account1.account_number,
            account3.account_number,
            20000.00,
            "Payment for services"
        )
        print(f"\n✅ Transfer result:")
        print(f"   {msg}")
        print(f"   Transaction Ref: {txn.reference_number}")

        # Refresh accounts
        account1 = banking_system.get_account(account1.account_number)
        account3 = banking_system.get_account(account3.account_number)

        print(f"\nAfter transfer:")
        print(f"  Account {account1.account_number} balance: HTG {account1.balance:,.2f}")
        print(f"  Account {account3.account_number} balance: HTG {account3.balance:,.2f}")

        # 6. International transfer
        print_section("6. INTERNATIONAL MONEY TRANSFER")

        # Refresh account
        account2 = banking_system.get_account(account2.account_number)
        print(f"Before international transfer:")
        print(f"  Account {account2.account_number} balance: HTG {account2.balance:,.2f}")

        success, msg, txn = transfer_system.transfer_international(
            account2.account_number,
            recipient_name="John Smith",
            recipient_bank="Bank of America",
            recipient_account="987654321",
            amount=13200.00,  # ~100 USD
            currency="USD",
            description="Family remittance"
        )
        print(f"\n✅ International transfer result:")
        print(f"   {msg}")
        print(f"   Transaction Ref: {txn.reference_number}")

        # Refresh account
        account2 = banking_system.get_account(account2.account_number)
        print(f"   New Balance: HTG {account2.balance:,.2f}")

        # 7. View transaction history
        print_section("7. TRANSACTION HISTORY")

        transactions = banking_system.get_account_transactions(account1.account_number, limit=10)
        print(f"Recent transactions for account {account1.account_number}:")
        for i, txn in enumerate(transactions, 1):
            print(f"\n  {i}. {txn.reference_number}")
            print(f"     Type: {txn.transaction_type}")
            print(f"     Amount: {txn.currency} {txn.amount:,.2f}")
            if txn.fee > 0:
                print(f"     Fee: HTG {txn.fee:,.2f}")
            print(f"     Date: {txn.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"     Description: {txn.description}")

        # 8. Check transfer limits
        print_section("8. DAILY TRANSFER LIMITS")

        summary = transfer_system.get_daily_transfer_summary(account1.account_number)
        print(f"Transfer limits for account {account1.account_number}:")
        print(f"  Daily Limit: HTG {summary['daily_limit']:,.2f}")
        print(f"  Used Today: HTG {summary['daily_total']:,.2f}")
        print(f"  Remaining: HTG {summary['remaining_limit']:,.2f}")

        # 9. View all accounts for a customer
        print_section("9. CUSTOMER ACCOUNTS SUMMARY")

        accounts = banking_system.get_customer_accounts(customer1.customer_id)
        print(f"Accounts for {customer1.get_full_name()}:")
        total_balance = 0
        for acc in accounts:
            print(f"\n  Account {acc.account_number}")
            print(f"    Type: {acc.account_type}")
            print(f"    Balance: {acc.currency} {acc.balance:,.2f}")
            print(f"    Status: {acc.status}")
            total_balance += acc.balance
        print(f"\n  Total Balance Across All Accounts: HTG {total_balance:,.2f}")

        # 10. Authentication demo
        print_section("10. AUTHENTICATION")

        # Successful login
        auth_customer = banking_system.authenticate_customer(
            customer1.email,
            "secure_password123"
        )
        if auth_customer:
            print(f"✅ Successfully authenticated: {auth_customer.get_full_name()}")
            session = banking_system.create_session(auth_customer.customer_id)
            print(f"   Session ID: {session.session_id}")
            print(f"   Login Time: {session.login_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Failed login
        auth_customer = banking_system.authenticate_customer(
            customer1.email,
            "wrong_password"
        )
        if not auth_customer:
            print("\n✅ Failed authentication with wrong password (as expected)")

        print_section("DEMO COMPLETED")
        print("\n✨ All features demonstrated successfully!")
        print("🚀 The Haiti Banking System is ready to use with Neon Postgres!")
        print("💾 All data is persisted in the database")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close database connections
        banking_system.close()


if __name__ == "__main__":
    demo()
