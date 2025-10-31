<?php
/**
 * Database Usage Examples
 *
 * Examples showing how to use the Database class
 */

require_once __DIR__ . '/../src/Database.php';

// Get database instance
$db = Database::getInstance();

echo "=== Database Usage Examples ===\n\n";

// Example 1: Create a calendar events table
echo "1. Creating calendar_events table...\n";
try {
    $db->execute("
        CREATE TABLE IF NOT EXISTS calendar_events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            location VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ");
    echo "   ✓ Table created successfully\n\n";
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

// Example 2: Insert a new event
echo "2. Inserting a new calendar event...\n";
try {
    $db->execute("
        INSERT INTO calendar_events (title, description, start_date, end_date, location)
        VALUES (?, ?, ?, ?, ?)
    ", [
        'Team Meeting',
        'Monthly team sync-up meeting',
        '2025-11-01 10:00:00',
        '2025-11-01 11:00:00',
        'Conference Room A'
    ]);
    $eventId = $db->lastInsertId('calendar_events_id_seq');
    echo "   ✓ Event created with ID: $eventId\n\n";
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

// Example 3: Fetch all events
echo "3. Fetching all calendar events...\n";
try {
    $events = $db->fetchAll("
        SELECT id, title, start_date, end_date, location
        FROM calendar_events
        ORDER BY start_date ASC
    ");

    if (empty($events)) {
        echo "   No events found\n\n";
    } else {
        foreach ($events as $event) {
            echo "   - [{$event['id']}] {$event['title']}\n";
            echo "     From: {$event['start_date']} To: {$event['end_date']}\n";
            echo "     Location: {$event['location']}\n";
        }
        echo "\n";
    }
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

// Example 4: Fetch a single event
echo "4. Fetching a specific event...\n";
try {
    $event = $db->fetchOne("
        SELECT * FROM calendar_events WHERE id = ?
    ", [1]);

    if ($event) {
        echo "   Event found:\n";
        echo "   Title: {$event['title']}\n";
        echo "   Description: {$event['description']}\n";
        echo "   Start: {$event['start_date']}\n";
        echo "   End: {$event['end_date']}\n\n";
    } else {
        echo "   Event not found\n\n";
    }
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

// Example 5: Update an event
echo "5. Updating an event...\n";
try {
    $affected = $db->execute("
        UPDATE calendar_events
        SET title = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ", ['Team Meeting (Updated)', 1]);
    echo "   ✓ Updated $affected row(s)\n\n";
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

// Example 6: Using transactions
echo "6. Using transactions...\n";
try {
    $db->beginTransaction();

    // Insert multiple events
    $db->execute("
        INSERT INTO calendar_events (title, description, start_date, end_date, location)
        VALUES (?, ?, ?, ?, ?)
    ", [
        'Project Deadline',
        'Final submission for Project X',
        '2025-11-15 23:59:59',
        '2025-11-15 23:59:59',
        'Online'
    ]);

    $db->execute("
        INSERT INTO calendar_events (title, description, start_date, end_date, location)
        VALUES (?, ?, ?, ?, ?)
    ", [
        'Code Review',
        'Review pending pull requests',
        '2025-11-02 14:00:00',
        '2025-11-02 15:00:00',
        'Virtual'
    ]);

    $db->commit();
    echo "   ✓ Transaction committed successfully\n\n";
} catch (Exception $e) {
    $db->rollback();
    echo "   ✗ Transaction rolled back: " . $e->getMessage() . "\n\n";
}

// Example 7: Count events
echo "7. Counting total events...\n";
try {
    $result = $db->fetchOne("SELECT COUNT(*) as total FROM calendar_events");
    echo "   Total events: {$result['total']}\n\n";
} catch (Exception $e) {
    echo "   ✗ Error: " . $e->getMessage() . "\n\n";
}

echo "=== Examples completed ===\n";
