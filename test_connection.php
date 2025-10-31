<?php
/**
 * Test Neon Database Connection
 *
 * This script tests the connection to your Neon PostgreSQL database
 */

require_once 'config/database.php';

echo "🔍 Testing Neon Database Connection...\n";
echo str_repeat("-", 50) . "\n";

$config = require 'config/database.php';

try {
    // Extract connection details from the connection string
    $connString = $config['connection_string'];

    // Parse the connection string to create a PDO DSN
    // Format: postgresql://user:password@host:port/database?params
    preg_match('/postgresql:\/\/([^:]+):([^@]+)@([^\/]+)\/([^?]+)(\?(.*))?/', $connString, $matches);

    if (count($matches) >= 5) {
        $user = $matches[1];
        $password = $matches[2];
        $hostPort = $matches[3];
        $database = $matches[4];

        // Parse host and port
        if (strpos($hostPort, ':') !== false) {
            list($host, $port) = explode(':', $hostPort);
        } else {
            $host = $hostPort;
            $port = 5432;
        }

        echo "Host: $host\n";
        echo "Port: $port\n";
        echo "Database: $database\n";
        echo "User: $user\n";
        echo str_repeat("-", 50) . "\n";

        // Create PDO connection
        $dsn = "pgsql:host=$host;port=$port;dbname=$database;sslmode=require";
        $pdo = new PDO($dsn, $user, $password, $config['options']);

        echo "✅ Connection successful!\n\n";

        // Test query to get PostgreSQL version
        $stmt = $pdo->query('SELECT version()');
        $version = $stmt->fetchColumn();
        echo "PostgreSQL Version:\n$version\n\n";

        // Get current database info
        $stmt = $pdo->query('SELECT current_database(), current_user, inet_server_addr(), inet_server_port()');
        $info = $stmt->fetch();
        echo "Current Database: " . $info['current_database'] . "\n";
        echo "Current User: " . $info['current_user'] . "\n";
        echo "Server Address: " . ($info['inet_server_addr'] ?? 'N/A') . "\n";
        echo "Server Port: " . ($info['inet_server_port'] ?? 'N/A') . "\n\n";

        // List existing tables
        $stmt = $pdo->query("SELECT tablename FROM pg_tables WHERE schemaname = 'public'");
        $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);

        echo "Existing tables in 'public' schema:\n";
        if (empty($tables)) {
            echo "  (No tables found - database is empty)\n";
        } else {
            foreach ($tables as $table) {
                echo "  - $table\n";
            }
        }

        echo "\n✅ All tests passed! Your Neon database is ready to use.\n";

    } else {
        throw new Exception("Could not parse connection string");
    }

} catch (PDOException $e) {
    echo "❌ Database connection failed!\n";
    echo "Error: " . $e->getMessage() . "\n";
    exit(1);
} catch (Exception $e) {
    echo "❌ Error: " . $e->getMessage() . "\n";
    exit(1);
}
