# Calendar Application

A PHP-based calendar application with Neon PostgreSQL database integration.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calendar
   ```

2. **Set up environment variables**
   - Copy your Neon database credentials to `.env` (already configured)
   - See `DATABASE_SETUP.md` for detailed instructions

3. **Test database connection**
   ```bash
   php test_connection.php
   ```

4. **View usage examples**
   ```bash
   php examples/database_usage.php
   ```

## 📁 Project Structure

```
calendar/
├── .env                    # Database credentials (not in git)
├── config/
│   └── database.php       # Database configuration
├── src/
│   └── Database.php       # Database wrapper class
├── examples/
│   └── database_usage.php # Usage examples
├── test_connection.php    # Connection test script
└── DATABASE_SETUP.md      # Complete database documentation
```

## 🔧 Database Configuration

This project uses **Neon PostgreSQL** as its database. All configuration is documented in `DATABASE_SETUP.md`.

### Quick Usage
```php
<?php
require_once 'src/Database.php';

$db = Database::getInstance();
$events = $db->fetchAll("SELECT * FROM calendar_events");
```

## 📚 Documentation

- [Database Setup & Usage](DATABASE_SETUP.md) - Complete guide to database configuration
- [Example Code](examples/database_usage.php) - Working examples

## 🔐 Security

- Never commit `.env` file (already in `.gitignore`)
- Always use prepared statements for queries
- Keep your Neon credentials secure

## 🛠️ Requirements

- PHP 7.4 or higher
- PostgreSQL PDO extension (`php-pgsql`)
- Neon PostgreSQL database account
