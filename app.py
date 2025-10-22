from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
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


# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city', 'Port-au-Prince')

        # Validate input
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))

        # Create new user
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

        # Create a default checking account
        account = Account(
            account_number=Account.generate_account_number(),
            account_type='checking',
            balance=0.0,
            user_id=user.id
        )
        db.session.add(account)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()

    # Get recent transactions
    recent_transactions = []
    for account in accounts:
        recent_transactions.extend(account.get_transaction_history(limit=10))

    recent_transactions.sort(key=lambda x: x.created_at, reverse=True)
    recent_transactions = recent_transactions[:10]

    total_balance = sum(account.balance for account in accounts)

    return render_template('dashboard.html',
                         accounts=accounts,
                         recent_transactions=recent_transactions,
                         total_balance=total_balance)


@app.route('/accounts')
@login_required
def accounts():
    user_accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('accounts.html', accounts=user_accounts)


@app.route('/accounts/create', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == 'POST':
        account_type = request.form.get('account_type')

        if account_type not in ['checking', 'savings']:
            flash('Invalid account type', 'error')
            return redirect(url_for('create_account'))

        account = Account(
            account_number=Account.generate_account_number(),
            account_type=account_type,
            balance=0.0,
            user_id=current_user.id
        )

        db.session.add(account)
        db.session.commit()

        flash(f'New {account_type} account created successfully!', 'success')
        return redirect(url_for('accounts'))

    return render_template('create_account.html')


@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    user_accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()

    if request.method == 'POST':
        from_account_id = request.form.get('from_account_id')
        to_account_number = request.form.get('to_account_number')
        amount = float(request.form.get('amount'))
        description = request.form.get('description', '')

        # Validate from account
        from_account = Account.query.get(from_account_id)
        if not from_account or from_account.user_id != current_user.id:
            flash('Invalid source account', 'error')
            return redirect(url_for('transfer'))

        # Validate to account
        to_account = Account.query.filter_by(account_number=to_account_number).first()
        if not to_account:
            flash('Recipient account not found', 'error')
            return redirect(url_for('transfer'))

        # Validate amount
        if amount < Config.MIN_TRANSFER_AMOUNT:
            flash(f'Minimum transfer amount is {Config.CURRENCY_SYMBOL}{Config.MIN_TRANSFER_AMOUNT}', 'error')
            return redirect(url_for('transfer'))

        if amount > Config.MAX_TRANSFER_AMOUNT:
            flash(f'Maximum transfer amount is {Config.CURRENCY_SYMBOL}{Config.MAX_TRANSFER_AMOUNT}', 'error')
            return redirect(url_for('transfer'))

        # Check balance
        if from_account.balance < amount:
            flash('Insufficient funds', 'error')
            return redirect(url_for('transfer'))

        # Perform transfer
        from_account.balance -= amount
        to_account.balance += amount

        # Create transaction record
        transaction = Transaction(
            transaction_id=Transaction.generate_transaction_id(),
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=amount,
            description=description,
            transaction_type='transfer',
            status='completed'
        )

        db.session.add(transaction)
        db.session.commit()

        flash(f'Transfer of {Config.CURRENCY_SYMBOL}{amount:,.2f} completed successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('transfer.html', accounts=user_accounts)


@app.route('/transactions')
@login_required
def transactions():
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [acc.id for acc in user_accounts]

    # Get all transactions
    all_transactions = Transaction.query.filter(
        (Transaction.from_account_id.in_(account_ids)) |
        (Transaction.to_account_id.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).all()

    return render_template('transactions.html', transactions=all_transactions)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.first_name = request.form.get('first_name', current_user.first_name)
    current_user.last_name = request.form.get('last_name', current_user.last_name)
    current_user.email = request.form.get('email', current_user.email)
    current_user.phone = request.form.get('phone', current_user.phone)
    current_user.address = request.form.get('address', current_user.address)
    current_user.city = request.form.get('city', current_user.city)

    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


# API Routes (for AJAX calls)
@app.route('/api/account/<account_number>')
@login_required
def api_get_account(account_number):
    account = Account.query.filter_by(account_number=account_number).first()
    if account:
        return jsonify({
            'success': True,
            'account_number': account.account_number,
            'owner_name': f'{account.owner.first_name} {account.owner.last_name}',
            'account_type': account.account_type
        })
    return jsonify({'success': False, 'message': 'Account not found'}), 404


# Initialize database
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    # Create admin user
    admin = User(
        username='admin',
        email='admin@haitibank.ht',
        first_name='Admin',
        last_name='User',
        phone='+509-1234-5678',
        address='123 Main Street',
        city='Port-au-Prince'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    # Create admin account with initial balance
    admin_account = Account(
        account_number=Account.generate_account_number(),
        account_type='checking',
        balance=100000.0,
        user_id=admin.id
    )
    db.session.add(admin_account)
    db.session.commit()

    print('Database seeded with sample data!')
    print('Admin username: admin')
    print('Admin password: admin123')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
