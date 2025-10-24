from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import random

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Account(db.Model):
    """Bank account model"""
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    account_type = db.Column(db.String(20), nullable=False)  # checking, savings
    balance = db.Column(db.Float, default=0.0)

    # Account ownership
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    transactions_sent = db.relationship('Transaction',
                                       foreign_keys='Transaction.from_account_id',
                                       backref='from_account',
                                       lazy=True)
    transactions_received = db.relationship('Transaction',
                                           foreign_keys='Transaction.to_account_id',
                                           backref='to_account',
                                           lazy=True)

    @staticmethod
    def generate_account_number():
        """Generate unique account number with Haiti prefix (509)"""
        while True:
            # Generate 13 random digits (509 + 13 = 16 total)
            number = '509' + ''.join([str(random.randint(0, 9)) for _ in range(13)])
            # Check if account number already exists
            if not Account.query.filter_by(account_number=number).first():
                return number

    def __repr__(self):
        return f'<Account {self.account_number}>'


class Transaction(db.Model):
    """Transaction model for money transfers"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    # Transaction details
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

    # Transaction metadata
    transaction_type = db.Column(db.String(20), default='transfer')  # transfer, deposit, withdrawal
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'
