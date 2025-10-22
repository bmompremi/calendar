# Haiti Banking System 2.0 - Testing Guide

## Pre-Test Setup

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python app.py
   # Or use: flask init-db
   ```

3. Seed with sample data (optional):
   ```bash
   flask seed-db
   ```

## Manual Testing Checklist

### 1. User Registration and Authentication

#### Test Registration
- [ ] Navigate to registration page
- [ ] Fill in all required fields
- [ ] Submit form
- [ ] Verify success message appears
- [ ] Verify default checking account is created
- [ ] Verify redirect to login page

#### Test Login
- [ ] Enter valid credentials
- [ ] Verify successful login
- [ ] Verify redirect to dashboard
- [ ] Check welcome message displays user's first name

#### Test Login Validation
- [ ] Try invalid username
- [ ] Try invalid password
- [ ] Verify error messages appear

#### Test Logout
- [ ] Click logout button
- [ ] Verify redirect to home page
- [ ] Verify logout message
- [ ] Try accessing protected pages (should redirect to login)

### 2. Dashboard

#### Test Dashboard Display
- [ ] Verify total balance shows correctly
- [ ] Verify number of accounts displays
- [ ] Verify recent transactions count
- [ ] Check all accounts are listed with correct balances
- [ ] Verify account numbers are displayed properly

### 3. Account Management

#### Test Create Account
- [ ] Navigate to "Create Account" page
- [ ] Select checking account type
- [ ] Submit form
- [ ] Verify success message
- [ ] Verify new account appears in account list
- [ ] Verify account number is unique and starts with "509"

#### Test Create Savings Account
- [ ] Create a savings account
- [ ] Verify it appears with correct type
- [ ] Verify initial balance is 0.00

#### Test Account Display
- [ ] View all accounts page
- [ ] Verify all accounts are listed
- [ ] Check account types are correct
- [ ] Verify balances match database
- [ ] Check created dates display correctly

### 4. Money Transfer

#### Test Valid Transfer
- [ ] Navigate to transfer page
- [ ] Select source account
- [ ] Enter valid recipient account number
- [ ] Verify account holder name appears
- [ ] Enter valid amount
- [ ] Add description
- [ ] Submit transfer
- [ ] Verify success message
- [ ] Check source account balance decreased
- [ ] Check recipient account balance increased
- [ ] Verify transaction appears in history

#### Test Transfer Validations
- [ ] Try transfer with insufficient funds
- [ ] Try transfer with amount less than minimum (< G1.00)
- [ ] Try transfer with amount greater than maximum (> G1,000,000)
- [ ] Try transfer to non-existent account
- [ ] Try transfer with negative amount
- [ ] Verify appropriate error messages for each case

#### Test Account Verification
- [ ] Enter recipient account number
- [ ] Blur the field (tab away)
- [ ] Verify account holder name appears
- [ ] Try invalid account number
- [ ] Verify "Account not found" message

#### Test Transfer Between Own Accounts
- [ ] Create two accounts
- [ ] Transfer between them
- [ ] Verify both balances update correctly

### 5. Transaction History

#### Test Transaction Display
- [ ] Navigate to transactions page
- [ ] Verify all transactions are listed
- [ ] Check dates are formatted correctly
- [ ] Verify transaction IDs are shown
- [ ] Check amounts show correct sign (+ or -)
- [ ] Verify color coding (red for debit, green for credit)

#### Test Transaction Details
- [ ] Check each transaction shows:
  - [ ] Transaction ID
  - [ ] Date and time
  - [ ] Transaction type
  - [ ] From account
  - [ ] To account
  - [ ] Amount
  - [ ] Description
  - [ ] Status

#### Test Recent Transactions on Dashboard
- [ ] Verify only last 10 transactions appear
- [ ] Check they are sorted by date (newest first)

### 6. User Profile

#### Test Profile Display
- [ ] Navigate to profile page
- [ ] Verify all user information displays correctly
- [ ] Check username is disabled (cannot be changed)
- [ ] Verify member since date is correct

#### Test Profile Update
- [ ] Change first name
- [ ] Change last name
- [ ] Update email
- [ ] Update phone number
- [ ] Update address
- [ ] Update city
- [ ] Submit changes
- [ ] Verify success message
- [ ] Refresh page and verify changes persisted
- [ ] Check updated info appears throughout the app

### 7. UI/UX Testing

#### Test Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768px width)
- [ ] Test on mobile (375px width)
- [ ] Verify navigation menu adapts
- [ ] Check all forms are usable on mobile

#### Test Navigation
- [ ] Click all menu items
- [ ] Verify correct pages load
- [ ] Check active states
- [ ] Test back button functionality

#### Test Flash Messages
- [ ] Verify success messages appear in green
- [ ] Verify error messages appear in red
- [ ] Check messages auto-dismiss after 5 seconds
- [ ] Verify messages can be manually dismissed

#### Test Visual Elements
- [ ] Check Haiti flag colors (blue and red)
- [ ] Verify consistent styling across pages
- [ ] Check buttons have hover effects
- [ ] Verify forms have focus states
- [ ] Test card shadows and borders

### 8. Security Testing

#### Test Authentication Protection
- [ ] Try accessing /dashboard without login
- [ ] Try accessing /transfer without login
- [ ] Try accessing /accounts without login
- [ ] Verify redirect to login page
- [ ] Verify return to intended page after login

#### Test Password Security
- [ ] Register new user
- [ ] Check database (password should be hashed)
- [ ] Verify password is not visible in any form
- [ ] Test password field is type="password"

#### Test Data Validation
- [ ] Try SQL injection in forms
- [ ] Try XSS in description fields
- [ ] Verify input sanitization
- [ ] Test maximum field lengths

### 9. Edge Cases

#### Test Large Numbers
- [ ] Try transfer with very large amount
- [ ] Verify decimal handling (2 decimal places)
- [ ] Test currency formatting

#### Test Special Characters
- [ ] Enter special characters in description
- [ ] Test names with accents (common in Haiti)
- [ ] Verify proper encoding

#### Test Concurrent Transfers
- [ ] Open two browser sessions
- [ ] Login as same user
- [ ] Try transfers from both sessions
- [ ] Verify balance consistency

### 10. Performance Testing

#### Test Page Load Times
- [ ] Measure dashboard load time
- [ ] Check transaction history with many records
- [ ] Test search/filter performance

#### Test Database Operations
- [ ] Create multiple accounts
- [ ] Perform many transfers
- [ ] Verify no slowdown

## Automated Testing (Future Enhancement)

### Unit Tests to Write
- User model tests
- Account model tests
- Transaction model tests
- Transfer validation tests
- Balance calculation tests

### Integration Tests to Write
- End-to-end registration flow
- Complete transfer flow
- Account creation flow
- Authentication flow

## Test Data

### Sample Users
```
User 1:
- Username: testuser1
- Email: test1@example.com
- Password: Test123!

User 2:
- Username: testuser2
- Email: test2@example.com
- Password: Test123!
```

### Sample Test Scenarios

#### Scenario 1: New User Journey
1. Register new account
2. Login
3. Create savings account
4. Check both accounts on dashboard
5. Logout

#### Scenario 2: Money Transfer
1. Login as User 1
2. Note account balance
3. Transfer G100 to User 2
4. Verify balance decreased
5. Check transaction history
6. Logout
7. Login as User 2
8. Verify balance increased
9. Check transaction history

#### Scenario 3: Multiple Accounts
1. Create 3 different accounts
2. Add funds to account 1
3. Transfer to account 2
4. Transfer from account 2 to account 3
5. Verify all balances
6. Check complete transaction history

## Bug Reporting

If you find bugs, report with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Browser and OS
- Screenshots if applicable
- Error messages

## Test Results Log

Date: ___________
Tester: ___________

| Test Category | Pass | Fail | Notes |
|--------------|------|------|-------|
| Registration |      |      |       |
| Login        |      |      |       |
| Dashboard    |      |      |       |
| Accounts     |      |      |       |
| Transfers    |      |      |       |
| Transactions |      |      |       |
| Profile      |      |      |       |
| UI/UX        |      |      |       |
| Security     |      |      |       |
| Edge Cases   |      |      |       |

Overall Status: ___________
