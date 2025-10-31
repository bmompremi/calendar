# Neon Database Configuration

This project is configured to use **Neon PostgreSQL** as its database.

## 🔧 Configuration Files

### 1. `.env` - Environment Variables
Contains your Neon database credentials (NOT committed to git):
```env
DATABASE_URL="postgresql://username:password@host/database?sslmode=require"
DB_HOST=your-host.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=username
DB_PASSWORD=password
```

### 2. `config/database.php` - Database Configuration
Loads environment variables and provides database configuration array.

### 3. `src/Database.php` - Database Wrapper Class
Simple PDO wrapper with convenient methods for database operations.

## 🚀 Usage

### Basic Connection
```php
<?php
require_once 'src/Database.php';

$db = Database::getInstance();
```

### Query Examples

#### Fetch All Rows
```php
$events = $db->fetchAll("SELECT * FROM calendar_events WHERE user_id = ?", [$userId]);
```

#### Fetch Single Row
```php
$event = $db->fetchOne("SELECT * FROM calendar_events WHERE id = ?", [$eventId]);
```

#### Insert Data
```php
$db->execute("
    INSERT INTO calendar_events (title, start_date, end_date)
    VALUES (?, ?, ?)
", ['Meeting', '2025-11-01 10:00:00', '2025-11-01 11:00:00']);

$newId = $db->lastInsertId('calendar_events_id_seq');
```

#### Update Data
```php
$affected = $db->execute("
    UPDATE calendar_events SET title = ? WHERE id = ?
", ['New Title', $eventId]);
```

#### Delete Data
```php
$affected = $db->execute("DELETE FROM calendar_events WHERE id = ?", [$eventId]);
```

### Transactions
```php
try {
    $db->beginTransaction();

    $db->execute("INSERT INTO ...", [...]);
    $db->execute("UPDATE ...", [...]);

    $db->commit();
} catch (Exception $e) {
    $db->rollback();
    throw $e;
}
```

## 📋 Database Schema for Calendar

### Calendar Events Table
```sql
CREATE TABLE calendar_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Users Table (Optional)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Event Participants Table (Optional)
```sql
CREATE TABLE event_participants (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES calendar_events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending', -- pending, accepted, declined
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id)
);
```

## 🧪 Testing the Connection

Run the test script to verify your database connection:
```bash
php test_connection.php
```

## 📚 Example Usage

Check out complete examples in:
```bash
php examples/database_usage.php
```

## 🔐 Security Notes

- The `.env` file is excluded from git (via `.gitignore`)
- Never commit database credentials
- Always use prepared statements (parameterized queries)
- The Database class uses PDO with prepared statements by default

## 🌐 Neon Dashboard

Access your database at: [https://console.neon.tech](https://console.neon.tech)

### Connection Details
- **Host**: ep-weathered-tooth-ada9j2ts-pooler.c-2.us-east-1.aws.neon.tech
- **Database**: neondb
- **User**: neondb_owner
- **Port**: 5432
- **SSL**: Required

## 🛠️ Common Operations

### Backup Database
```bash
# Install PostgreSQL client tools first
pg_dump -h your-host.neon.tech -U username -d database > backup.sql
```

### View Tables
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

### View Table Structure
```sql
\d table_name  -- In psql
-- OR
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'your_table';
```

## 🐛 Troubleshooting

### Connection Issues
1. Verify your `.env` file exists and has correct credentials
2. Check that your IP is allowed in Neon's firewall settings
3. Ensure SSL is enabled (Neon requires SSL)

### Query Issues
- Always use prepared statements with `?` placeholders
- Check error messages: `$e->getMessage()`
- Enable error logging in production

## 📖 Additional Resources

- [Neon Documentation](https://neon.tech/docs)
- [PHP PDO Documentation](https://www.php.net/manual/en/book.pdo.php)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
