from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50), default='Port-au-Prince')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    accounts = db.relationship('Account', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)  # 'checking', 'savings'
    balance = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

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
        """Generate a unique 16-digit account number"""
        prefix = "509"  # Haiti country code
        random_digits = ''.join(random.choices(string.digits, k=13))
        return prefix + random_digits

    def get_transaction_history(self, limit=50):
        """Get all transactions for this account"""
        sent = Transaction.query.filter_by(from_account_id=self.id).all()
        received = Transaction.query.filter_by(to_account_id=self.id).all()
        all_transactions = sent + received
        all_transactions.sort(key=lambda x: x.created_at, reverse=True)
        return all_transactions[:limit]

    def __repr__(self):
        return f'<Account {self.account_number}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), unique=True, nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    transaction_type = db.Column(db.String(20), default='transfer')  # 'transfer', 'deposit', 'withdrawal'
    status = db.Column(db.String(20), default='completed')  # 'completed', 'pending', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_transaction_id():
        """Generate a unique transaction ID"""
        import uuid
        return str(uuid.uuid4())

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'
