# Haiti Banking System 2.0 - Deployment & Database Setup Guide

## Quick Start - Copy and Use

### Option 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/bmompremi/calendar.git haiti-banking-system
cd haiti-banking-system

# Checkout the banking system branch
git checkout claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e
```

### Option 2: Download as ZIP

1. Go to: https://github.com/bmompremi/calendar
2. Switch to branch: `claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e`
3. Click "Code" → "Download ZIP"
4. Extract to your desired location

---

## Database Configuration

### Using SQLite (Default - No Setup Required)

SQLite is already configured and requires no installation. Perfect for:
- Development
- Testing
- Small deployments
- Single-server setups

**No changes needed!** Just run:
```bash
python app.py
```

The database file `haiti_bank.db` will be created automatically.

---

### Using PostgreSQL (Recommended for Production)

#### Step 1: Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download from: https://www.postgresql.org/download/windows/

#### Step 2: Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE haiti_bank;
CREATE USER bankadmin WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE haiti_bank TO bankadmin;
\q
```

#### Step 3: Update Configuration

Edit `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # PostgreSQL Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://bankadmin:your_secure_password@localhost:5432/haiti_bank'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BANK_NAME = "Haiti National Bank"
    CURRENCY = "HTG"
    CURRENCY_SYMBOL = "G"
    MIN_TRANSFER_AMOUNT = 1.0
    MAX_TRANSFER_AMOUNT = 1000000.0
```

#### Step 4: Install PostgreSQL Driver

```bash
pip install psycopg2-binary
```

Update `requirements.txt`:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
python-dotenv==1.0.0
psycopg2-binary==2.9.9
```

---

### Using MySQL/MariaDB

#### Step 1: Install MySQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

#### Step 2: Create Database

```bash
# Login to MySQL
sudo mysql -u root -p

# Create database and user
CREATE DATABASE haiti_bank CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bankadmin'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON haiti_bank.* TO 'bankadmin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Step 3: Update Configuration

Edit `config.py`:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://bankadmin:your_secure_password@localhost:3306/haiti_bank'
```

#### Step 4: Install MySQL Driver

```bash
pip install pymysql cryptography
```

Update `requirements.txt`:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
python-dotenv==1.0.0
PyMySQL==1.1.0
cryptography==41.0.7
```

---

## Environment Configuration (.env file)

### Step 1: Create .env file

```bash
cp .env.example .env
```

### Step 2: Edit .env file

**For SQLite:**
```env
SECRET_KEY=your-super-secret-random-key-here-change-this
DATABASE_URL=sqlite:///haiti_bank.db
FLASK_ENV=production
```

**For PostgreSQL:**
```env
SECRET_KEY=your-super-secret-random-key-here-change-this
DATABASE_URL=postgresql://bankadmin:your_secure_password@localhost:5432/haiti_bank
FLASK_ENV=production
```

**For MySQL:**
```env
SECRET_KEY=your-super-secret-random-key-here-change-this
DATABASE_URL=mysql+pymysql://bankadmin:your_secure_password@localhost:3306/haiti_bank
FLASK_ENV=production
```

**For Remote Database:**
```env
SECRET_KEY=your-super-secret-random-key-here-change-this
DATABASE_URL=postgresql://user:password@hostname:5432/database_name
FLASK_ENV=production
```

### Step 3: Generate Secure SECRET_KEY

```python
# Run in Python to generate a secure key
import secrets
print(secrets.token_hex(32))
```

---

## Installation Steps

### 1. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database

Create and edit your `.env` file as shown above.

### 4. Initialize Database

```bash
# Method 1: Using Flask CLI
flask init-db

# Method 2: Using Python
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

# Method 3: Just run the app (auto-creates)
python app.py
```

### 5. Seed Sample Data (Optional)

```bash
flask seed-db
```

This creates:
- Admin username: `admin`
- Admin password: `admin123`
- Admin account with G100,000 balance

### 6. Run the Application

```bash
# Development mode
python app.py

# Or with Flask CLI
flask run

# Production mode (see Production Deployment section)
```

Access at: `http://localhost:5000`

---

## Using Cloud Databases

### Heroku Postgres

```env
DATABASE_URL=postgres://username:password@hostname.compute.amazonaws.com:5432/database_name
```

**Note:** Heroku provides DATABASE_URL automatically. Just use:
```python
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
```

### AWS RDS (PostgreSQL/MySQL)

```env
# PostgreSQL
DATABASE_URL=postgresql://admin:password@your-instance.region.rds.amazonaws.com:5432/haiti_bank

# MySQL
DATABASE_URL=mysql+pymysql://admin:password@your-instance.region.rds.amazonaws.com:3306/haiti_bank
```

### Google Cloud SQL

```env
DATABASE_URL=postgresql://user:password@/haiti_bank?host=/cloudsql/project:region:instance
```

### Azure Database

```env
DATABASE_URL=postgresql://user@server:password@server.postgres.database.azure.com:5432/haiti_bank?sslmode=require
```

---

## Migration from SQLite to PostgreSQL/MySQL

### Step 1: Export Data from SQLite

```bash
# Install sqlite3 command line tool
sudo apt install sqlite3

# Export schema
sqlite3 haiti_bank.db .schema > schema.sql

# Export data
sqlite3 haiti_bank.db .dump > data.sql
```

### Step 2: Convert and Import

**For PostgreSQL:**
```bash
# Clean up SQLite-specific syntax
sed -i 's/AUTOINCREMENT/SERIAL/g' schema.sql

# Import to PostgreSQL
psql -U bankadmin -d haiti_bank -f schema.sql
```

**For MySQL:**
```bash
# Convert SQLite dump to MySQL
# Manual editing may be required

mysql -u bankadmin -p haiti_bank < data.sql
```

### Step 3: Alternative - Use Python Script

```python
# migrate_db.py
from app import app, db
from models import User, Account, Transaction
import sqlite3

def migrate_from_sqlite():
    # Connect to old SQLite database
    old_db = sqlite3.connect('haiti_bank.db')
    cursor = old_db.cursor()

    with app.app_context():
        # Clear new database
        db.drop_all()
        db.create_all()

        # Migrate users
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            # Create user objects and add to new DB
            pass  # Implement based on your schema

        db.session.commit()

    old_db.close()
    print("Migration complete!")

if __name__ == '__main__':
    migrate_from_sqlite()
```

---

## Production Deployment

### Using Gunicorn (Production WSGI Server)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With more options
gunicorn -w 4 -b 0.0.0.0:8000 --access-logfile - --error-logfile - app:app
```

### Using Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/haiti-bank`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/haiti-banking-system/static;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/haiti-bank /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service

Create `/etc/systemd/system/haiti-bank.service`:

```ini
[Unit]
Description=Haiti Banking System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/haiti-banking-system
Environment="PATH=/var/www/haiti-banking-system/venv/bin"
ExecStart=/var/www/haiti-banking-system/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl start haiti-bank
sudo systemctl enable haiti-bank
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://bankadmin:password@db:5432/haiti_bank
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=haiti_bank
      - POSTGRES_USER=bankadmin
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

---

## Troubleshooting

### Database Connection Errors

**PostgreSQL:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U bankadmin -d haiti_bank -h localhost
```

**MySQL:**
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Check connection
mysql -u bankadmin -p haiti_bank
```

### Permission Errors

```bash
# PostgreSQL
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE haiti_bank TO bankadmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bankadmin;

# MySQL
GRANT ALL PRIVILEGES ON haiti_bank.* TO 'bankadmin'@'localhost';
FLUSH PRIVILEGES;
```

### Module Not Found Errors

```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Already Exists Error

```bash
# Drop and recreate database
# PostgreSQL:
sudo -u postgres psql
DROP DATABASE haiti_bank;
CREATE DATABASE haiti_bank;

# MySQL:
DROP DATABASE haiti_bank;
CREATE DATABASE haiti_bank;
```

---

## Security Checklist for Production

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Use a production database (PostgreSQL/MySQL)
- [ ] Set FLASK_ENV=production
- [ ] Disable debug mode
- [ ] Use strong database passwords
- [ ] Implement rate limiting
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Use secure session cookies
- [ ] Implement logging and monitoring
- [ ] Regular security updates

---

## Backup and Restore

### PostgreSQL Backup

```bash
# Backup
pg_dump -U bankadmin -d haiti_bank -f backup_$(date +%Y%m%d).sql

# Restore
psql -U bankadmin -d haiti_bank -f backup_20231201.sql
```

### MySQL Backup

```bash
# Backup
mysqldump -u bankadmin -p haiti_bank > backup_$(date +%Y%m%d).sql

# Restore
mysql -u bankadmin -p haiti_bank < backup_20231201.sql
```

### SQLite Backup

```bash
# Simple copy
cp haiti_bank.db haiti_bank_backup_$(date +%Y%m%d).db

# Or using SQLite
sqlite3 haiti_bank.db ".backup 'backup.db'"
```

---

## Support

If you encounter issues:
1. Check the error logs
2. Verify database connection
3. Ensure all dependencies are installed
4. Check file permissions
5. Review the TESTING.md guide
6. Create an issue on GitHub

---

## Quick Reference Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env file

# Initialize
flask init-db
flask seed-db

# Run
python app.py

# Production
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
