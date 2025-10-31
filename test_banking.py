#!/usr/bin/env python3
"""
Test script for the Banking Management System
Tests all core functionality to ensure everything works correctly.
"""

import os
from banking_system import Bank


def test_banking_system():
    """Run comprehensive tests on the banking system."""
    print("=" * 60)
    print("Banking Management System - Test Suite")
    print("=" * 60)
    print()

    # Remove existing test data if present
    test_file = "test_bank_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"Removed existing test file: {test_file}")

    # Initialize bank
    print("1. Initializing Bank...")
    bank = Bank("Test Bank", test_file)
    print(f"   ✓ Bank created: {bank.name}")
    print()

    # Test customer creation
    print("2. Creating Customers...")
    customer1 = bank.create_customer(
        "Alice Smith",
        "alice@example.com",
        "555-0001",
        "123 Main St"
    )
    print(f"   ✓ Customer 1 created: {customer1.name} (ID: {customer1.customer_id})")

    customer2 = bank.create_customer(
        "Bob Johnson",
        "bob@example.com",
        "555-0002",
        "456 Oak Ave"
    )
    print(f"   ✓ Customer 2 created: {customer2.name} (ID: {customer2.customer_id})")
    print()

    # Test account creation
    print("3. Creating Accounts...")
    account1 = bank.create_account(customer1.customer_id, "savings", 1000.0)
    print(f"   ✓ Savings account created: {account1.account_number} with ${account1.balance:.2f}")

    account2 = bank.create_account(customer1.customer_id, "checking", 500.0)
    print(f"   ✓ Checking account created: {account2.account_number} with ${account2.balance:.2f}")

    account3 = bank.create_account(customer2.customer_id, "business", 2000.0)
    print(f"   ✓ Business account created: {account3.account_number} with ${account3.balance:.2f}")
    print()

    # Test deposits
    print("4. Testing Deposits...")
    account1.deposit(500.0, "Test deposit")
    print(f"   ✓ Deposited $500 to {account1.account_number}")
    print(f"   ✓ New balance: ${account1.balance:.2f}")

    account2.deposit(250.0, "Another deposit")
    print(f"   ✓ Deposited $250 to {account2.account_number}")
    print(f"   ✓ New balance: ${account2.balance:.2f}")
    print()

    # Test withdrawals
    print("5. Testing Withdrawals...")
    account1.withdraw(200.0, "Test withdrawal")
    print(f"   ✓ Withdrew $200 from {account1.account_number}")
    print(f"   ✓ New balance: ${account1.balance:.2f}")

    # Test insufficient funds
    try:
        account2.withdraw(10000.0, "Too much")
        print("   ✗ ERROR: Should have raised insufficient funds error!")
    except ValueError as e:
        print(f"   ✓ Insufficient funds protection working: {e}")
    print()

    # Test transfers
    print("6. Testing Transfers...")
    initial_balance_1 = account1.balance
    initial_balance_3 = account3.balance

    bank.transfer(account1.account_number, account3.account_number, 300.0, "Test transfer")
    print(f"   ✓ Transferred $300 from {account1.account_number} to {account3.account_number}")
    print(f"   ✓ Account 1: ${initial_balance_1:.2f} → ${account1.balance:.2f}")
    print(f"   ✓ Account 3: ${initial_balance_3:.2f} → ${account3.balance:.2f}")
    print()

    # Test transaction history
    print("7. Testing Transaction History...")
    transactions = account1.get_transaction_history()
    print(f"   ✓ Account {account1.account_number} has {len(transactions)} transactions")
    for i, trans in enumerate(transactions, 1):
        print(f"     {i}. {trans}")
    print()

    # Test customer operations
    print("8. Testing Customer Operations...")
    all_accounts = customer1.get_all_accounts()
    print(f"   ✓ Customer 1 has {len(all_accounts)} accounts")

    total_balance = customer1.get_total_balance()
    print(f"   ✓ Customer 1 total balance: ${total_balance:.2f}")
    print()

    # Test bank summary
    print("9. Testing Bank Summary...")
    summary = bank.get_bank_summary()
    print(f"   ✓ Total Customers: {summary['total_customers']}")
    print(f"   ✓ Total Accounts: {summary['total_accounts']}")
    print(f"   ✓ Total Deposits: ${summary['total_deposits']:.2f}")
    print()

    # Test data persistence
    print("10. Testing Data Persistence...")
    bank.save_data()
    print(f"   ✓ Data saved to {test_file}")

    # Load data in new bank instance
    bank2 = Bank("Test Bank 2", test_file)
    print(f"   ✓ Data loaded in new bank instance")

    loaded_customer = bank2.get_customer(customer1.customer_id)
    if loaded_customer:
        print(f"   ✓ Customer data persisted: {loaded_customer.name}")
        print(f"   ✓ Customer has {len(loaded_customer.accounts)} accounts")
    else:
        print("   ✗ ERROR: Customer data not loaded!")

    loaded_account = bank2.get_account(account1.account_number)
    if loaded_account:
        print(f"   ✓ Account data persisted: {loaded_account.account_number}")
        print(f"   ✓ Balance: ${loaded_account.balance:.2f}")
        print(f"   ✓ Transactions: {len(loaded_account.transactions)}")
    else:
        print("   ✗ ERROR: Account data not loaded!")
    print()

    # Test error handling
    print("11. Testing Error Handling...")

    # Invalid account type
    try:
        bank.create_account(customer1.customer_id, "invalid", 100.0)
        print("   ✗ ERROR: Should reject invalid account type!")
    except ValueError as e:
        print(f"   ✓ Invalid account type rejected: {e}")

    # Negative deposit
    try:
        account1.deposit(-100.0, "Negative")
        print("   ✗ ERROR: Should reject negative deposits!")
    except ValueError as e:
        print(f"   ✓ Negative deposit rejected: {e}")

    # Negative withdrawal
    try:
        account1.withdraw(-50.0, "Negative")
        print("   ✗ ERROR: Should reject negative withdrawals!")
    except ValueError as e:
        print(f"   ✓ Negative withdrawal rejected: {e}")

    # Invalid customer
    try:
        bank.create_account("INVALID123", "savings", 100.0)
        print("   ✗ ERROR: Should reject invalid customer ID!")
    except ValueError as e:
        print(f"   ✓ Invalid customer ID rejected: {e}")
    print()

    # Final summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Bank Name: {bank.name}")
    print(f"Customers: {len(bank.customers)}")
    print(f"Total Accounts Created: {bank.account_counter - 1000}")
    print(f"Data File: {test_file}")
    print()
    print("✓ All tests completed successfully!")
    print("=" * 60)

    # Clean up test file
    print()
    cleanup = input("Remove test data file? (y/n): ")
    if cleanup.lower() == 'y':
        os.remove(test_file)
        print(f"✓ Test file {test_file} removed")
    else:
        print(f"Test file {test_file} kept for inspection")


if __name__ == "__main__":
    try:
        test_banking_system()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
