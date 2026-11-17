#!/usr/bin/env python3
"""
Full database migration script to properly update the schema
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import json
from datetime import datetime

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
            print("Checking current task table structure...")

            # Get all current task data to preserve it
            print("Backing up existing task data...")
            cur.execute("SELECT * FROM task;")
            rows = cur.fetchall()

            # Get column names
            col_names = [desc[0] for desc in cur.description]
            print(f"Current columns: {col_names}")

            # If the table has data, backup to a temporary table
            if rows:
                print(f"Found {len(rows)} existing tasks. Backing up...")

                # Create backup table
                cur.execute("""
                    CREATE TEMPORARY TABLE task_backup AS SELECT * FROM task;
                """)

                # Drop the original task table
                cur.execute("DROP TABLE task CASCADE;")

                # Now recreate the task table with the new schema using SQLModel
                from sqlmodel import SQLModel
                from src.models import Task
                from src.database import engine

                # This will recreate the table with the new schema
                SQLModel.metadata.tables[Task.__tablename__].create(engine, checkfirst=True)

                print("Task table recreated with new schema.")

                # Restore the data to the new table structure
                cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'task';")
                new_columns = [row[0] for row in cur.fetchall()]

                # Prepare column mapping - only copy existing columns
                existing_cols_in_backup = [col for col in new_columns if col in col_names]

                # Build insert statement for existing columns
                existing_placeholders = ', '.join(['%s'] * len(existing_cols_in_backup))
                existing_columns_str = ', '.join(existing_cols_in_backup)

                # Get data from backup table
                backup_col_placeholders = ', '.join(['%s'] * len(col_names))
                backup_columns_str = ', '.join(col_names)

                # Query from backup
                cur.execute(f"SELECT {backup_columns_str} FROM task_backup;")
                backup_rows = cur.fetchall()

                # Insert into new table (only existing columns)
                for row in backup_rows:
                    # Map row values to only the columns that exist in the new table
                    mapped_values = []
                    for col in existing_cols_in_backup:
                        col_idx = col_names.index(col)
                        mapped_values.append(row[col_idx])

                    cur.execute(
                        f"INSERT INTO task ({existing_columns_str}) VALUES ({existing_placeholders});",
                        tuple(mapped_values)
                    )

                print(f"Restored {len(backup_rows)} tasks to the new table structure.")

            else:
                # If no data exists, just recreate the table
                from sqlmodel import SQLModel
                from src.models import Task
                from src.database import engine

                SQLModel.metadata.tables[Task.__tablename__].create(engine, checkfirst=True)
                print("Task table created with new schema (empty).")

            conn.commit()
            print("Database schema updated successfully!")

        except Exception as e:
            print(f"Error during schema migration: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Could not parse PostgreSQL URL")
else:
    print("Not a PostgreSQL database")