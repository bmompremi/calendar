"""
Configuration settings for Haiti Banking Management System
"""

# Supported currencies
CURRENCIES = {
    'HTG': 'Haitian Gourde',
    'USD': 'US Dollar'
}

# Default currency for Haiti
DEFAULT_CURRENCY = 'HTG'

# Exchange rates (HTG to other currencies)
# Updated: October 23, 2025
EXCHANGE_RATES = {
    'HTG': 1.0,
    'USD': 0.007655  # Current rate: 1 USD = 130.64 HTG (Oct 2025)
}

# Transaction limits
MAX_DAILY_TRANSFER_LIMIT = 500000  # HTG
MAX_SINGLE_TRANSFER_LIMIT = 100000  # HTG
MIN_TRANSFER_AMOUNT = 10  # HTG

# Account settings
MIN_ACCOUNT_BALANCE = 0
INITIAL_ACCOUNT_NUMBER = 1000000

# Haiti banking institutions
HAITI_BANKS = [
    'Banque de la République d\'Haïti (BRH)',
    'Banque Nationale de Crédit (BNC)',
    'Capital Bank',
    'Sogebank',
    'Unibank',
    'Banque Populaire Haïtienne (BPH)',
    'Citibank Haiti',
    'Banque de l\'Union Haïtienne (BUH)'
]

# Transaction types
TRANSACTION_TYPES = [
    'DEPOSIT',
    'WITHDRAWAL',
    'TRANSFER_SENT',
    'TRANSFER_RECEIVED',
    'TRANSFER_INTERNATIONAL'
]

# Account types
ACCOUNT_TYPES = [
    'SAVINGS',
    'CHECKING',
    'BUSINESS'
]
