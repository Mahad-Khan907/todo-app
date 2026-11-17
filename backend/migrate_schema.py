#!/usr/bin/env python3
"""
Script to migrate the database schema by adding missing columns to the task table
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

if DATABASE_URL.startswith("postgresql"):
    # Parse PostgreSQL URL
    import re
    match = re.match(r"postgresql://([^:]+):([^@]+)@([^/]+)/(.+)\?", DATABASE_URL)
    if match:
        username = match.group(1)
        password = match.group(2)
        host_info = match.group(3)
        database_name = match.group(4)

        # Split host and port
        if ':' in host_info:
            host, port = host_info.split(':')
        else:
            host = host_info
            port = '5432'

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database_name,
            user=username,
            password=password
        )

        cur = conn.cursor()

        try:
            # Check if columns exist first
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='task' AND column_name='recurrence_id';
            """)

            columns_exist = cur.fetchone()

            if not columns_exist:
                print("Adding missing columns to task table...")

                # Add missing columns
                alter_queries = [
                    "ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_id VARCHAR;",
                    "ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_at TIMESTAMP;",
                    "ALTER TABLE task ADD COLUMN IF NOT EXISTS last_notified TIMESTAMP;",
                    "ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE;",
                    "ALTER TABLE task ADD COLUMN IF NOT EXISTS last_occurrence_processed TIMESTAMP;"
                ]

                for query in alter_queries:
                    print(f"Executing: {query}")
                    cur.execute(query)

                conn.commit()
                print("Schema migration completed successfully!")
            else:
                print("Columns already exist in the task table.")

        except Exception as e:
            print(f"Error during schema migration: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Could not parse PostgreSQL URL")
else:
    print("Not a PostgreSQL database, migration script only supports PostgreSQL")