#!/usr/bin/env python3
"""
Script to manually add the missing column to the database
"""

import os
from dotenv import load_dotenv
import psycopg2
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

if DATABASE_URL.startswith("postgresql"):
    # Parse PostgreSQL URL using urllib
    parsed_url = urlparse(DATABASE_URL)

    conn = psycopg2.connect(
        host=parsed_url.hostname,
        port=parsed_url.port,
        database=parsed_url.path.lstrip('/'),
        user=parsed_url.username,
        password=parsed_url.password,
        sslmode='require'  # Neon requires SSL
    )

    cur = conn.cursor()

    try:
        print("Attempting to add missing column to task table...")

        # Check if the column already exists
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='task' AND column_name='last_occurrence_processed';
        """)

        result = cur.fetchone()

        if result:
            print("Column 'last_occurrence_processed' already exists.")
        else:
            print("Adding column 'last_occurrence_processed' to task table...")

            # Add the missing column
            cur.execute("ALTER TABLE task ADD COLUMN last_occurrence_processed TIMESTAMP;")

            print("Column 'last_occurrence_processed' added successfully!")

        # Commit the changes
        conn.commit()
        print("Database schema update completed successfully!")

    except Exception as e:
        print(f"Error during schema update: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
else:
    print("Not a PostgreSQL database")