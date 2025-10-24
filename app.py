from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Account, Transaction
from config import Config
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================================
# ROUTES - Authentication
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')

        # Validation
        if not all([username, email, password, first_name, last_name]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')

        # Create user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ROUTES - Dashboard & Profile
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    total_balance = sum(account.balance for account in accounts)

    # Get recent transactions
    recent_transactions = []
    for account in accounts:
        transactions = Transaction.query.filter(
            (Transaction.from_account_id == account.id) |
            (Transaction.to_account_id == account.id)
        ).order_by(Transaction.created_at.desc()).limit(5).all()
        recent_transactions.extend(transactions)

    # Sort by date and get top 5
    recent_transactions.sort(key=lambda x: x.created_at, reverse=True)
    recent_transactions = recent_transactions[:5]

    return render_template('dashboard.html',
                         accounts=accounts,
                         total_balance=total_balance,
                         recent_transactions=recent_transactions)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')


# ============================================================================
# ROUTES - Account Management
# ============================================================================

@app.route('/accounts')
@login_required
def accounts():
    """View all user accounts"""
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('accounts.html', accounts=user_accounts)


@app.route('/accounts/create', methods=['GET', 'POST'])
@login_required
def create_account():
    """Create new account"""
    if request.method == 'POST':
        account_type = request.form.get('account_type')

        if account_type not in ['checking', 'savings']:
            flash('Invalid account type.', 'error')
            return render_template('create_account.html')

        # Create account
        account = Account(
            account_number=Account.generate_account_number(),
            account_type=account_type,
            user_id=current_user.id
        )

        db.session.add(account)
        db.session.commit()

        flash(f'{account_type.capitalize()} account created successfully! Account number: {account.account_number}', 'success')
        return redirect(url_for('accounts'))

    return render_template('create_account.html')


# ============================================================================
# ROUTES - Money Transfer
# ============================================================================

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    """Money transfer between accounts"""
    user_accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()

    if request.method == 'POST':
        from_account_id = request.form.get('from_account')
        to_account_number = request.form.get('to_account')
        amount = request.form.get('amount')
        description = request.form.get('description', '')

        # Validation
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            flash('Invalid amount.', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        if amount < Config.MIN_TRANSFER_AMOUNT:
            flash(f'Minimum transfer amount is {Config.CURRENCY_SYMBOL} {Config.MIN_TRANSFER_AMOUNT:.2f}', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        if amount > Config.MAX_TRANSFER_AMOUNT:
            flash(f'Maximum transfer amount is {Config.CURRENCY_SYMBOL} {Config.MAX_TRANSFER_AMOUNT:,.2f}', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        # Get sender account
        from_account = Account.query.filter_by(
            id=from_account_id,
            user_id=current_user.id,
            is_active=True
        ).first()

        if not from_account:
            flash('Invalid sender account.', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        # Check balance
        if from_account.balance < amount:
            flash('Insufficient balance.', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        # Get recipient account
        to_account = Account.query.filter_by(
            account_number=to_account_number,
            is_active=True
        ).first()

        if not to_account:
            flash('Recipient account not found.', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        if from_account.id == to_account.id:
            flash('Cannot transfer to the same account.', 'error')
            return render_template('transfer.html', accounts=user_accounts)

        # Process transfer
        from_account.balance -= amount
        to_account.balance += amount

        # Create transaction record
        transaction = Transaction(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=amount,
            description=description,
            transaction_type='transfer',
            status='completed'
        )

        db.session.add(transaction)
        db.session.commit()

        flash(f'Transfer of {Config.CURRENCY_SYMBOL} {amount:,.2f} completed successfully!', 'success')
        return redirect(url_for('transactions'))

    return render_template('transfer.html', accounts=user_accounts)


@app.route('/transactions')
@login_required
def transactions():
    """View transaction history"""
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [account.id for account in user_accounts]

    # Get all transactions for user's accounts
    all_transactions = Transaction.query.filter(
        (Transaction.from_account_id.in_(account_ids)) |
        (Transaction.to_account_id.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).all()

    return render_template('transactions.html', transactions=all_transactions)


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/account/<account_number>')
@login_required
def api_get_account(account_number):
    """API endpoint to verify account number"""
    account = Account.query.filter_by(account_number=account_number, is_active=True).first()

    if account:
        return jsonify({
            'success': True,
            'account_number': account.account_number,
            'account_type': account.account_type,
            'owner_name': f"{account.owner.first_name} {account.owner.last_name}"
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Account not found'
        }), 404


# ============================================================================
# CLI COMMANDS
# ============================================================================

@app.cli.command('init-db')
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized successfully!")


@app.cli.command('seed-db')
def seed_db():
    """Seed database with sample data"""
    # Create admin user
    admin = User(
        username='admin',
        email='admin@haitibank.ht',
        first_name='Admin',
        last_name='User',
        phone='+509 1234 5678',
        address='Port-au-Prince',
        city='Port-au-Prince'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    # Create sample account
    account = Account(
        account_number=Account.generate_account_number(),
        account_type='checking',
        balance=10000.0,
        user_id=admin.id
    )
    db.session.add(account)
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Admin username: admin")
    print(f"Admin password: admin123")
    print(f"Admin account: {account.account_number}")


# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('currency')
def currency_filter(value):
    """Format value as currency"""
    return f"{Config.CURRENCY_SYMBOL} {value:,.2f}"


@app.context_processor
def inject_config():
    """Inject config into templates"""
    return {
        'BANK_NAME': Config.BANK_NAME,
        'CURRENCY': Config.CURRENCY,
        'CURRENCY_SYMBOL': Config.CURRENCY_SYMBOL
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
