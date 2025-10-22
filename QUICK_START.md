# Haiti Banking System 2.0 - Quick Start Guide

## 🚀 Copy and Use in 5 Minutes

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
git clone https://github.com/bmompremi/calendar.git haiti-bank
cd haiti-bank
git checkout claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e
```

**Option B: Download ZIP**
1. Visit: https://github.com/bmompremi/calendar
2. Switch to branch: `claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e`
3. Click "Code" → "Download ZIP"
4. Extract and navigate to folder

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

### Step 3: Choose Your Database

#### 🟢 EASIEST: SQLite (No Setup Required)

```bash
# Just run the app - database creates automatically!
python app.py
```

✅ That's it! Access at http://localhost:5000

---

#### 🟡 RECOMMENDED: PostgreSQL

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Windows - Download from postgresql.org
```

**Create Database:**
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE haiti_bank;
CREATE USER bankadmin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE haiti_bank TO bankadmin;
\q
```

**Configure Application:**
```bash
# Run the interactive setup
python setup_database.py

# OR manually create .env file:
cat > .env << 'EOF'
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://bankadmin:your_password@localhost:5432/haiti_bank
FLASK_ENV=production
EOF
```

**Install PostgreSQL Driver:**
```bash
pip install psycopg2-binary
```

**Initialize and Run:**
```bash
python app.py
```

✅ Access at http://localhost:5000

---

#### 🟠 MySQL/MariaDB

**Install MySQL:**
```bash
# Ubuntu/Debian
sudo apt install mysql-server

# macOS
brew install mysql
brew services start mysql
```

**Create Database:**
```bash
sudo mysql -u root -p
```
```sql
CREATE DATABASE haiti_bank;
CREATE USER 'bankadmin'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON haiti_bank.* TO 'bankadmin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Configure Application:**
```bash
# Run the interactive setup
python setup_database.py

# OR manually:
cat > .env << 'EOF'
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://bankadmin:your_password@localhost:3306/haiti_bank
FLASK_ENV=production
EOF
```

**Install MySQL Driver:**
```bash
pip install pymysql cryptography
```

**Initialize and Run:**
```bash
python app.py
```

✅ Access at http://localhost:5000

---

## 🎯 Using Existing Database

### Connect to Your Database

Edit `.env` file and change `DATABASE_URL`:

**PostgreSQL on remote server:**
```env
DATABASE_URL=postgresql://user:password@your-server.com:5432/database_name
```

**MySQL on remote server:**
```env
DATABASE_URL=mysql+pymysql://user:password@your-server.com:3306/database_name
```

**Cloud databases:**
```env
# Heroku Postgres
DATABASE_URL=postgres://username:password@host.compute.amazonaws.com:5432/dbname

# AWS RDS
DATABASE_URL=postgresql://admin:password@instance.region.rds.amazonaws.com:5432/haiti_bank

# Google Cloud SQL
DATABASE_URL=postgresql://user:password@/haiti_bank?host=/cloudsql/project:region:instance
```

### Initialize Tables

```bash
python app.py
# Tables will be created automatically on first run

# OR manually:
flask init-db
```

---

## 🎁 Interactive Setup (Recommended)

The easiest way to set up any database:

```bash
python setup_database.py
```

This interactive script will:
- ✅ Help you choose your database type
- ✅ Generate a secure secret key
- ✅ Create the .env configuration file
- ✅ Test database connection
- ✅ Initialize database tables
- ✅ Create demo admin account (optional)

---

## 📝 Create Demo Account

**Option 1: Using Flask CLI**
```bash
flask seed-db
```

**Option 2: During interactive setup**
```bash
python setup_database.py
# Choose "yes" when asked about demo account
```

**Option 3: Manual registration**
```bash
python app.py
# Go to http://localhost:5000
# Click "Register" and create your account
```

**Demo Credentials (if using seed):**
- Username: `admin`
- Password: `admin123`
- Balance: G100,000.00

---

## 🔧 Complete Installation Commands

**For SQLite (Easiest):**
```bash
git clone https://github.com/bmompremi/calendar.git haiti-bank
cd haiti-bank
git checkout claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**For PostgreSQL (Recommended):**
```bash
# 1. Get the code
git clone https://github.com/bmompremi/calendar.git haiti-bank
cd haiti-bank
git checkout claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e

# 2. Set up Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary

# 3. Set up PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE haiti_bank;"
sudo -u postgres psql -c "CREATE USER bankadmin WITH PASSWORD 'mypassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE haiti_bank TO bankadmin;"

# 4. Configure application
python setup_database.py
# Follow the prompts

# 5. Run
python app.py
```

**For MySQL:**
```bash
# 1. Get the code
git clone https://github.com/bmompremi/calendar.git haiti-bank
cd haiti-bank
git checkout claude/haiti-banking-system-v2-011CUK4o8coQ9bs5ZJK6wm8e

# 2. Set up Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pymysql cryptography

# 3. Set up MySQL
sudo mysql -e "CREATE DATABASE haiti_bank;"
sudo mysql -e "CREATE USER 'bankadmin'@'localhost' IDENTIFIED BY 'mypassword';"
sudo mysql -e "GRANT ALL PRIVILEGES ON haiti_bank.* TO 'bankadmin'@'localhost';"

# 4. Configure application
python setup_database.py
# Follow the prompts

# 5. Run
python app.py
```

---

## ✅ Verify Installation

After installation, verify everything works:

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Check the output:**
   ```
   * Running on http://127.0.0.1:5000
   ```

3. **Open browser:**
   Visit: http://localhost:5000

4. **Register or login:**
   - Click "Register" to create new account
   - Or use demo account if created

5. **Test features:**
   - ✅ View dashboard
   - ✅ Create new account
   - ✅ Make a transfer
   - ✅ View transactions

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### "Database connection failed"
```bash
# Check if database server is running
# PostgreSQL:
sudo systemctl status postgresql

# MySQL:
sudo systemctl status mysql

# Verify credentials in .env file
```

### "Could not create database"
```bash
# Create database manually first
# Then run: python app.py
```

### "Port 5000 already in use"
```bash
# Change port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Permission denied"
```bash
# Grant database permissions
# PostgreSQL:
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE haiti_bank TO bankadmin;

# MySQL:
GRANT ALL PRIVILEGES ON haiti_bank.* TO 'bankadmin'@'localhost';
```

---

## 📚 Next Steps

After successful installation:

1. **Review Documentation:**
   - `README.md` - Overview and features
   - `DEPLOYMENT_GUIDE.md` - Production deployment
   - `TESTING.md` - Testing checklist

2. **Customize Settings:**
   - Edit `config.py` for bank name, currency, limits
   - Update `.env` for security settings

3. **Deploy to Production:**
   - See `DEPLOYMENT_GUIDE.md`
   - Use Gunicorn + Nginx
   - Enable HTTPS
   - Set up backups

4. **Add Features:**
   - Modify `models.py` for new data models
   - Add routes in `app.py`
   - Create templates in `templates/`

---

## 🆘 Get Help

- **Documentation:** Read DEPLOYMENT_GUIDE.md
- **Testing:** See TESTING.md
- **Issues:** Check error logs in terminal
- **Support:** Create GitHub issue

---

## 📋 Summary Checklist

- [ ] Code downloaded/cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database chosen and configured
- [ ] .env file created
- [ ] Database initialized
- [ ] Application running
- [ ] Accessible in browser
- [ ] Demo account working (if created)
- [ ] All features tested

---

## 🎉 Success!

If you can:
- ✅ Access http://localhost:5000
- ✅ Register a new user
- ✅ Create accounts
- ✅ Transfer money
- ✅ View transactions

**Congratulations! Your Haiti Banking System 2.0 is ready to use!**
