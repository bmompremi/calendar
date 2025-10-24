import os
from datetime import timedelta

class Config:
    """Application configuration"""

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///haiti_bank.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Bank configuration
    BANK_NAME = "Haiti National Bank"
    CURRENCY = "HTG"
    CURRENCY_SYMBOL = "G"

    # Transfer limits
    MIN_TRANSFER_AMOUNT = 1.0
    MAX_TRANSFER_AMOUNT = 1000000.0

    # Account number configuration
    ACCOUNT_NUMBER_PREFIX = "509"  # Haiti country code
    ACCOUNT_NUMBER_LENGTH = 16
