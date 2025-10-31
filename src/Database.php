<?php
/**
 * Database Connection Wrapper
 *
 * Simple PDO wrapper for Neon PostgreSQL database
 */

class Database {
    private static $instance = null;
    private $pdo;

    private function __construct() {
        $config = require dirname(__DIR__) . '/config/database.php';

        // Parse connection string
        $connString = $config['connection_string'];
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

            // Create PDO connection
            $dsn = "pgsql:host=$host;port=$port;dbname=$database;sslmode=require";
            $this->pdo = new PDO($dsn, $user, $password, $config['options']);
        } else {
            throw new Exception("Invalid connection string format");
        }
    }

    /**
     * Get singleton instance
     */
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Get PDO connection
     */
    public function getConnection() {
        return $this->pdo;
    }

    /**
     * Execute a query and return results
     */
    public function query($sql, $params = []) {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt;
    }

    /**
     * Execute query and fetch all results
     */
    public function fetchAll($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetchAll();
    }

    /**
     * Execute query and fetch single row
     */
    public function fetchOne($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetch();
    }

    /**
     * Execute query and return affected rows
     */
    public function execute($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->rowCount();
    }

    /**
     * Get last inserted ID
     */
    public function lastInsertId($sequence = null) {
        return $this->pdo->lastInsertId($sequence);
    }

    /**
     * Begin transaction
     */
    public function beginTransaction() {
        return $this->pdo->beginTransaction();
    }

    /**
     * Commit transaction
     */
    public function commit() {
        return $this->pdo->commit();
    }

    /**
     * Rollback transaction
     */
    public function rollback() {
        return $this->pdo->rollBack();
    }
}
