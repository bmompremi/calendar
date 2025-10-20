# Haiti Banking System - Neon Postgres Setup Guide

This guide will help you set up the Haiti Banking Management System with Neon Postgres database for cloud-based persistence.

## What is Neon?

[Neon](https://neon.tech) is a serverless Postgres database platform that offers:
- **Serverless Architecture**: Auto-scaling and pay-per-use
- **Instant Provisioning**: Create databases in seconds
- **Branching**: Database branching for development/testing
- **Global Deployment**: Low-latency access worldwide
- **Free Tier**: Generous free tier for development

## Prerequisites

- Python 3.8 or higher
- A Neon account (sign up at https://neon.tech)
- Git (for cloning the repository)

## Step 1: Create a Neon Database

### 1.1 Sign up for Neon

1. Go to https://neon.tech
2. Click "Sign Up" and create a free account
3. Verify your email address

### 1.2 Create a New Project

1. Log into the Neon Console
2. Click "New Project"
3. Enter project details:
   - **Project Name**: `haiti-banking-system`
   - **Region**: Choose closest to your location (e.g., `us-east-2`)
   - **Postgres Version**: 16 (recommended)
4. Click "Create Project"

### 1.3 Get Your Connection String

After creating the project, you'll see a connection string like:

```
postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/banking_db?sslmode=require
```

**Save this connection string** - you'll need it in Step 3.

## Step 2: Install the Application

### 2.1 Clone the Repository

```bash
git clone <repository-url>
cd calendar
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management
- `bcrypt` - Password hashing
- `pydantic` - Data validation

## Step 3: Configure Database Connection

### 3.1 Create Environment File

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

### 3.2 Edit `.env` File

Open `.env` and add your Neon connection string:

```env
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/banking_db?sslmode=require
```

**Important**: Replace with your actual Neon connection string from Step 1.3

### 3.3 Secure Your Environment File

Make sure `.env` is in `.gitignore`:

```bash
echo ".env" >> .gitignore
```

## Step 4: Initialize the Database

### 4.1 Test Database Connection

```bash
python init_db.py --test
```

You should see:
```
✅ Connection successful!
📌 PostgreSQL version: PostgreSQL 16.x...
```

### 4.2 Create Database Schema

```bash
python init_db.py
```

This will:
- Create all necessary tables (customers, accounts, transactions, sessions)
- Set up indexes for performance
- Create views for reporting
- Initialize sequences for account numbers

You should see output like:
```
🔌 Connecting to Neon Postgres database...
✅ Connected successfully!
📋 Initializing database schema...
✅ Database schema created successfully!

📊 Created 4 tables:
   - accounts
   - customers
   - sessions
   - transactions

🔢 Created 1 sequence(s):
   - account_number_seq

👁️  Created 2 view(s):
   - customer_account_summary
   - daily_transaction_summary

✨ Database initialization complete!
🚀 Your Haiti Banking System is ready to use with Neon Postgres!
```

## Step 5: Run the Application

### 5.1 Run the Demo

Test the system with demo data:

```bash
python demo_db.py
```

This will demonstrate:
- Customer creation
- Account opening
- Deposits and withdrawals
- Domestic and international transfers
- Transaction history
- Authentication

### 5.2 Run the CLI Application

Start the interactive banking CLI:

```bash
python main_db.py
```

You'll see:
```
============================================================
          HAITI BANKING MANAGEMENT SYSTEM
               Sistèm Bankè Ayiti
             (Powered by Neon Postgres)
============================================================

🌟 Welcome to Haiti Banking Management System
   Byenveni nan Sistèm Jesyon Bankè Ayiti

🚀 Connected to Neon Postgres Database

--- MAIN MENU ---
1. Register New Customer
2. Login
3. Exit
```

## Step 6: Using the System

### Register a New Customer

1. Choose option `1` from the main menu
2. Enter customer details:
   - First Name, Last Name
   - Email (must be unique)
   - Phone, Address, City, Country
   - Date of Birth (YYYY-MM-DD format)
   - National ID (Haiti NIF)
   - Password (will be securely hashed)

### Create a Bank Account

1. Login with your email and password
2. Choose option `2` (Create New Account)
3. Select account type: SAVINGS, CHECKING, or BUSINESS
4. Choose currency: HTG or USD
5. Enter initial deposit amount

### Perform Banking Operations

- **Deposits**: Option 3
- **Withdrawals**: Option 4
- **Domestic Transfers**: Option 5
- **International Transfers**: Option 6
- **View Transactions**: Option 7
- **Account Statement**: Option 8
- **Check Transfer Limits**: Option 9

## Database Features

### Tables

1. **customers**: Customer information and credentials
2. **accounts**: Bank accounts with balances
3. **transactions**: All banking transactions (audit trail)
4. **sessions**: Active user sessions

### Views

1. **customer_account_summary**: Account summaries per customer
2. **daily_transaction_summary**: Daily transaction statistics

### Security Features

- SSL/TLS encryption (required by Neon)
- Bcrypt password hashing
- Session management with timeouts
- Transaction validation and limits
- Audit trail for all operations

## Neon Console Features

### Viewing Data

1. Log into Neon Console
2. Go to your project
3. Click "Tables" to view data
4. Click "SQL Editor" to run queries

### Example Queries

```sql
-- View all customers
SELECT * FROM customers;

-- View all accounts with balances
SELECT a.account_number, c.first_name, c.last_name,
       a.account_type, a.balance, a.currency
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id;

-- View recent transactions
SELECT * FROM transactions
ORDER BY timestamp DESC
LIMIT 10;

-- Customer account summary
SELECT * FROM customer_account_summary;

-- Daily transaction summary
SELECT * FROM daily_transaction_summary
ORDER BY transaction_date DESC;
```

### Database Branching

Neon supports database branching for development:

```bash
# Create a development branch
neonctl branches create --name dev

# Get connection string for dev branch
neonctl connection-string dev
```

## Monitoring

### Neon Dashboard

The Neon Console provides:
- Query performance metrics
- Storage usage
- Connection statistics
- Error logs

### Application Logs

Monitor your application logs for:
- Failed transactions
- Authentication attempts
- Error messages

## Backup and Recovery

### Automatic Backups

Neon automatically:
- Takes continuous backups
- Provides point-in-time recovery
- Retains backups based on your plan

### Manual Export

Export data using `pg_dump`:

```bash
pg_dump $DATABASE_URL > backup.sql
```

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to database

**Solutions**:
1. Verify DATABASE_URL in `.env` file
2. Check Neon project is active in console
3. Ensure `sslmode=require` is in connection string
4. Verify network/firewall settings

### Schema Errors

**Problem**: Tables already exist

**Solution**: Drop and recreate schema:

```bash
# Connect to database
psql $DATABASE_URL

# Drop schema
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

# Exit and reinitialize
\q
python init_db.py
```

### Performance Issues

**Solutions**:
1. Check Neon dashboard for query performance
2. Verify indexes are created properly
3. Consider upgrading Neon plan for more resources

## Production Deployment

### Environment Variables

For production, use environment variables instead of `.env`:

```bash
export DATABASE_URL="postgresql://..."
python main_db.py
```

### Security Checklist

- [ ] Use strong passwords for database
- [ ] Enable Neon IP allowlist (if needed)
- [ ] Rotate database credentials regularly
- [ ] Monitor authentication logs
- [ ] Set up alerts for suspicious activity
- [ ] Regular backups verification

### Scaling

Neon auto-scales, but for high traffic:
1. Upgrade to Neon Pro plan
2. Configure connection pooling
3. Consider read replicas for reporting

## Support

### Neon Support

- Documentation: https://neon.tech/docs
- Discord: https://discord.gg/neon
- Email: support@neon.tech

### Application Support

For issues with the banking system:
- Check logs in the console
- Review transaction history
- Contact system administrator

## Next Steps

1. ✅ Set up development environment
2. ✅ Create test accounts and transactions
3. ✅ Explore all features in CLI
4. 📚 Read API documentation
5. 🔒 Review security best practices
6. 🚀 Deploy to production

## Additional Resources

- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Haiti Banking Regulations](https://www.brh.ht/)

---

**System Status**: ✅ Production Ready with Neon Postgres

**Last Updated**: 2025-10-20
