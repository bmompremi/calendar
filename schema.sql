-- Haiti Banking Management System - Database Schema for Neon Postgres

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Customers table
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    national_id VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_national_id ON customers(national_id);

-- Accounts table
CREATE TABLE accounts (
    account_number VARCHAR(50) PRIMARY KEY,
    customer_id UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('SAVINGS', 'CHECKING', 'BUSINESS')),
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'HTG',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'SUSPENDED', 'CLOSED')),
    daily_transfer_total DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    last_transfer_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_accounts_customer_id ON accounts(customer_id);
CREATE INDEX idx_accounts_status ON accounts(status);

-- Transactions table
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    from_account VARCHAR(50) REFERENCES accounts(account_number),
    to_account VARCHAR(50),
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    transaction_type VARCHAR(30) NOT NULL CHECK (transaction_type IN (
        'DEPOSIT', 'WITHDRAWAL', 'TRANSFER_SENT', 'TRANSFER_RECEIVED', 'TRANSFER_INTERNATIONAL'
    )),
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED' CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    fee DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    exchange_rate DECIMAL(10, 6) NOT NULL DEFAULT 1.000000,
    reference_number VARCHAR(50) UNIQUE NOT NULL
);

-- Create indexes for transaction queries
CREATE INDEX idx_transactions_from_account ON transactions(from_account);
CREATE INDEX idx_transactions_to_account ON transactions(to_account);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC);
CREATE INDEX idx_transactions_reference_number ON transactions(reference_number);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);

-- Sessions table
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create index on customer_id and session status
CREATE INDEX idx_sessions_customer_id ON sessions(customer_id);
CREATE INDEX idx_sessions_active ON sessions(is_active, last_activity);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a sequence for account numbers
CREATE SEQUENCE account_number_seq START WITH 1000000;

-- Function to generate next account number
CREATE OR REPLACE FUNCTION next_account_number()
RETURNS VARCHAR AS $$
BEGIN
    RETURN nextval('account_number_seq')::VARCHAR;
END;
$$ LANGUAGE plpgsql;

-- View for account balances summary
CREATE OR REPLACE VIEW customer_account_summary AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    COUNT(a.account_number) as total_accounts,
    SUM(CASE WHEN a.currency = 'HTG' THEN a.balance ELSE 0 END) as total_htg_balance,
    SUM(CASE WHEN a.currency = 'USD' THEN a.balance ELSE 0 END) as total_usd_balance
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
WHERE a.status = 'ACTIVE'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email;

-- View for daily transaction summary
CREATE OR REPLACE VIEW daily_transaction_summary AS
SELECT
    DATE(timestamp) as transaction_date,
    transaction_type,
    currency,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    SUM(fee) as total_fees
FROM transactions
WHERE status = 'COMPLETED'
GROUP BY DATE(timestamp), transaction_type, currency
ORDER BY transaction_date DESC, transaction_type;

-- Sample data validation function
CREATE OR REPLACE FUNCTION validate_transfer(
    p_from_account VARCHAR,
    p_amount DECIMAL
)
RETURNS BOOLEAN AS $$
DECLARE
    v_balance DECIMAL;
BEGIN
    -- Get current balance
    SELECT balance INTO v_balance
    FROM accounts
    WHERE account_number = p_from_account AND status = 'ACTIVE';

    -- Check if account exists and has sufficient balance
    IF v_balance IS NULL THEN
        RETURN FALSE;
    END IF;

    IF v_balance < p_amount THEN
        RETURN FALSE;
    END IF;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Grant necessary permissions (adjust based on your Neon user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_neon_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_neon_user;

-- Comments for documentation
COMMENT ON TABLE customers IS 'Stores customer information and credentials';
COMMENT ON TABLE accounts IS 'Stores bank account information';
COMMENT ON TABLE transactions IS 'Stores all banking transactions';
COMMENT ON TABLE sessions IS 'Stores active user sessions';
COMMENT ON VIEW customer_account_summary IS 'Summary of customer accounts and balances';
COMMENT ON VIEW daily_transaction_summary IS 'Daily transaction statistics';
