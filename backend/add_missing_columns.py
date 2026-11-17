#!/usr/bin/env python3
"""
Direct script to add missing columns to the task table
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from src.database import DATABASE_URL


def add_missing_columns():
    """Add the missing columns directly to the database"""
    engine = create_engine(DATABASE_URL)

    # SQL statements to add missing columns
    sql_statements = [
        "ALTER TABLE task ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE task ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(50);",
        "ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_at TIMESTAMP WITH TIME ZONE;",
        "ALTER TABLE task ADD COLUMN IF NOT EXISTS last_notified TIMESTAMP WITH TIME ZONE;"
    ]

    print("Adding missing columns to the task table...")

    with engine.connect() as conn:
        transaction = conn.begin()

        try:
            for sql in sql_statements:
                print(f"Executing: {sql}")
                conn.execute(text(sql))

            transaction.commit()
            print("All missing columns added successfully!")

        except Exception as e:
            print(f"Error adding columns: {e}")
            transaction.rollback()
            raise


def verify_columns():
    """Verify that the columns have been added"""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Query to check if columns exist
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'task'
            AND column_name IN ('is_recurring', 'recurring_pattern', 'reminder_at', 'last_notified')
            ORDER BY column_name;
        """))

        columns = result.fetchall()

        print("\nColumns in task table:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")


if __name__ == "__main__":
    add_missing_columns()
    verify_columns()
    print("\nDatabase schema updated successfully!")