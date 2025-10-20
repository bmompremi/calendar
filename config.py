import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///haiti_bank.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BANK_NAME = "Haiti National Bank"
    CURRENCY = "HTG"  # Haitian Gourde
    CURRENCY_SYMBOL = "G"
    MIN_TRANSFER_AMOUNT = 1.0
    MAX_TRANSFER_AMOUNT = 1000000.0
