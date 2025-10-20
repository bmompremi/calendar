"""
Database connection and operations for Neon Postgres
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Manages connection to Neon Postgres database"""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database connection

        Args:
            connection_string: PostgreSQL connection string. If None, reads from DATABASE_URL env var
        """
        self.connection_string = connection_string or os.getenv('DATABASE_URL')

        if not self.connection_string:
            raise ValueError(
                "Database connection string not provided. "
                "Set DATABASE_URL environment variable or pass connection_string parameter."
            )

        # Create connection pool (min 1, max 10 connections)
        self.pool = SimpleConnectionPool(1, 10, self.connection_string)

    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor):
        """Get a cursor from a connection"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
            finally:
                cursor.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a SELECT query and return results as list of dicts"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        """Execute a SELECT query and return one result as dict"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute a query multiple times with different parameters"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

    def close(self):
        """Close all connections in the pool"""
        if self.pool:
            self.pool.closeall()


class DatabaseManager:
    """High-level database operations for banking system"""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    # ==================== Customer Operations ====================

    def create_customer(self, customer_data: Dict) -> Dict:
        """Create a new customer"""
        query = """
            INSERT INTO customers (
                customer_id, first_name, last_name, email, phone,
                address, city, country, date_of_birth, national_id, password_hash
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            customer_data['customer_id'],
            customer_data['first_name'],
            customer_data['last_name'],
            customer_data['email'],
            customer_data['phone'],
            customer_data['address'],
            customer_data['city'],
            customer_data['country'],
            customer_data['date_of_birth'],
            customer_data['national_id'],
            customer_data['password_hash']
        )
        return self.db.execute_one(query, params)

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        """Get customer by ID"""
        query = "SELECT * FROM customers WHERE customer_id = %s"
        return self.db.execute_one(query, (customer_id,))

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        """Get customer by email"""
        query = "SELECT * FROM customers WHERE email = %s"
        return self.db.execute_one(query, (email,))

    def update_customer(self, customer_id: str, updates: Dict) -> int:
        """Update customer information"""
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        query = f"UPDATE customers SET {set_clause} WHERE customer_id = %s"
        params = tuple(updates.values()) + (customer_id,)
        return self.db.execute_update(query, params)

    # ==================== Account Operations ====================

    def create_account(self, account_data: Dict) -> Dict:
        """Create a new account"""
        # Get next account number from sequence
        account_number = self.db.execute_one("SELECT next_account_number() as number")['number']

        query = """
            INSERT INTO accounts (
                account_number, customer_id, account_type, balance,
                currency, status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            account_number,
            account_data['customer_id'],
            account_data['account_type'],
            account_data['balance'],
            account_data['currency'],
            account_data['status']
        )
        return self.db.execute_one(query, params)

    def get_account(self, account_number: str) -> Optional[Dict]:
        """Get account by account number"""
        query = "SELECT * FROM accounts WHERE account_number = %s"
        return self.db.execute_one(query, (account_number,))

    def get_customer_accounts(self, customer_id: str) -> List[Dict]:
        """Get all accounts for a customer"""
        query = "SELECT * FROM accounts WHERE customer_id = %s ORDER BY created_at DESC"
        return self.db.execute_query(query, (customer_id,))

    def update_account_balance(self, account_number: str, new_balance: float) -> int:
        """Update account balance"""
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
        return self.db.execute_update(query, (new_balance, account_number))

    def update_account(self, account_number: str, updates: Dict) -> int:
        """Update account information"""
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        query = f"UPDATE accounts SET {set_clause} WHERE account_number = %s"
        params = tuple(updates.values()) + (account_number,)
        return self.db.execute_update(query, params)

    def update_daily_transfer_total(self, account_number: str, amount: float, timestamp) -> int:
        """Update daily transfer total for an account"""
        query = """
            UPDATE accounts
            SET daily_transfer_total = daily_transfer_total + %s,
                last_transfer_date = %s
            WHERE account_number = %s
        """
        return self.db.execute_update(query, (amount, timestamp, account_number))

    def reset_daily_transfer_total(self, account_number: str) -> int:
        """Reset daily transfer total"""
        query = """
            UPDATE accounts
            SET daily_transfer_total = 0,
                last_transfer_date = NULL
            WHERE account_number = %s
        """
        return self.db.execute_update(query, (account_number,))

    # ==================== Transaction Operations ====================

    def create_transaction(self, transaction_data: Dict) -> Dict:
        """Create a new transaction"""
        query = """
            INSERT INTO transactions (
                transaction_id, from_account, to_account, amount, currency,
                transaction_type, status, description, fee, exchange_rate, reference_number
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            transaction_data['transaction_id'],
            transaction_data.get('from_account'),
            transaction_data.get('to_account'),
            transaction_data['amount'],
            transaction_data['currency'],
            transaction_data['transaction_type'],
            transaction_data['status'],
            transaction_data['description'],
            transaction_data.get('fee', 0.0),
            transaction_data.get('exchange_rate', 1.0),
            transaction_data['reference_number']
        )
        return self.db.execute_one(query, params)

    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Get transaction by ID"""
        query = "SELECT * FROM transactions WHERE transaction_id = %s"
        return self.db.execute_one(query, (transaction_id,))

    def get_account_transactions(self, account_number: str, limit: int = 10) -> List[Dict]:
        """Get recent transactions for an account"""
        query = """
            SELECT * FROM transactions
            WHERE from_account = %s OR to_account = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (account_number, account_number, limit))

    def get_account_statement(self, account_number: str, start_date, end_date) -> List[Dict]:
        """Get account statement for a date range"""
        query = """
            SELECT * FROM transactions
            WHERE (from_account = %s OR to_account = %s)
                AND timestamp >= %s
                AND timestamp <= %s
            ORDER BY timestamp ASC
        """
        return self.db.execute_query(query, (account_number, account_number, start_date, end_date))

    def get_transfer_history(self, account_number: str, cutoff_date) -> List[Dict]:
        """Get transfer history since cutoff date"""
        query = """
            SELECT * FROM transactions
            WHERE (from_account = %s OR to_account = %s)
                AND transaction_type IN ('TRANSFER_SENT', 'TRANSFER_RECEIVED', 'TRANSFER_INTERNATIONAL')
                AND timestamp >= %s
            ORDER BY timestamp DESC
        """
        return self.db.execute_query(query, (account_number, account_number, cutoff_date))

    # ==================== Session Operations ====================

    def create_session(self, session_data: Dict) -> Dict:
        """Create a new session"""
        query = """
            INSERT INTO sessions (session_id, customer_id)
            VALUES (%s, %s)
            RETURNING *
        """
        params = (session_data['session_id'], session_data['customer_id'])
        return self.db.execute_one(query, params)

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        query = "SELECT * FROM sessions WHERE session_id = %s"
        return self.db.execute_one(query, (session_id,))

    def update_session_activity(self, session_id: str) -> int:
        """Update session last activity time"""
        query = "UPDATE sessions SET last_activity = CURRENT_TIMESTAMP WHERE session_id = %s"
        return self.db.execute_update(query, (session_id,))

    def end_session(self, session_id: str) -> int:
        """End a session"""
        query = "UPDATE sessions SET is_active = FALSE WHERE session_id = %s"
        return self.db.execute_update(query, (session_id,))

    def cleanup_expired_sessions(self, timeout_minutes: int = 30) -> int:
        """Cleanup expired sessions"""
        query = """
            UPDATE sessions
            SET is_active = FALSE
            WHERE is_active = TRUE
                AND last_activity < CURRENT_TIMESTAMP - INTERVAL '%s minutes'
        """
        return self.db.execute_update(query, (timeout_minutes,))

    # ==================== Utility Operations ====================

    def get_customer_summary(self, customer_id: str) -> Optional[Dict]:
        """Get customer account summary"""
        query = "SELECT * FROM customer_account_summary WHERE customer_id = %s"
        return self.db.execute_one(query, (customer_id,))

    def get_daily_summary(self, date) -> List[Dict]:
        """Get daily transaction summary"""
        query = "SELECT * FROM daily_transaction_summary WHERE transaction_date = %s"
        return self.db.execute_query(query, (date,))
