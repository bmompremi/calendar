#!/usr/bin/env python3
"""
Database Initialization Script for Haiti Banking System with Neon Postgres
Run this script to set up the database schema
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def init_database(connection_string: str = None):
    """
    Initialize the database with the schema

    Args:
        connection_string: PostgreSQL connection string. If None, reads from DATABASE_URL
    """
    conn_string = connection_string or os.getenv('DATABASE_URL')

    if not conn_string:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("\nPlease create a .env file with your Neon database connection string:")
        print("DATABASE_URL=postgresql://username:password@host/database?sslmode=require")
        sys.exit(1)

    print("🔌 Connecting to Neon Postgres database...")

    try:
        # Connect to database
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()

        print("✅ Connected successfully!")
        print("\n📋 Initializing database schema...")

        # Read schema file
        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_file, 'r') as f:
            schema_sql = f.read()

        # Execute schema
        cursor.execute(schema_sql)

        print("✅ Database schema created successfully!")

        # Verify tables were created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")

        # Check sequences
        cursor.execute("""
            SELECT sequence_name
            FROM information_schema.sequences
            WHERE sequence_schema = 'public';
        """)

        sequences = cursor.fetchall()
        if sequences:
            print(f"\n🔢 Created {len(sequences)} sequence(s):")
            for seq in sequences:
                print(f"   - {seq[0]}")

        # Check views
        cursor.execute("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema = 'public';
        """)

        views = cursor.fetchall()
        if views:
            print(f"\n👁️  Created {len(views)} view(s):")
            for view in views:
                print(f"   - {view[0]}")

        print("\n✨ Database initialization complete!")
        print("\n🚀 Your Haiti Banking System is ready to use with Neon Postgres!")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ Error: schema.sql file not found")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def test_connection(connection_string: str = None):
    """Test database connection"""
    conn_string = connection_string or os.getenv('DATABASE_URL')

    if not conn_string:
        print("❌ Error: DATABASE_URL environment variable not set")
        return False

    print("🔌 Testing connection to Neon Postgres...")

    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        print(f"✅ Connection successful!")
        print(f"📌 PostgreSQL version: {version[:50]}...")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"❌ Connection failed: {e}")
        return False


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Initialize Haiti Banking System database on Neon Postgres'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test database connection only'
    )
    parser.add_argument(
        '--connection-string',
        type=str,
        help='Database connection string (overrides DATABASE_URL env var)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print(" " * 10 + "HAITI BANKING SYSTEM")
    print(" " * 8 + "Database Initialization")
    print("=" * 60)
    print()

    if args.test:
        # Test connection only
        if test_connection(args.connection_string):
            print("\n✅ Database is ready for initialization!")
        else:
            sys.exit(1)
    else:
        # Initialize database
        init_database(args.connection_string)


if __name__ == "__main__":
    main()
