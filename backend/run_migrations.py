#!/usr/bin/env python3
"""
Script to run database migrations for Phase 5 features
Adds the required columns for recurring tasks and reminders to the database
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect
from sqlmodel import SQLModel
from src.models import Task
from src.database import DATABASE_URL


def check_current_schema():
    """Check the current database schema"""
    engine = create_engine(DATABASE_URL)

    inspector = inspect(engine)
    columns = inspector.get_columns('task')

    print("Current 'task' table columns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")

    # Check for required columns
    required_cols = ['is_recurring', 'recurring_pattern', 'reminder_at', 'last_notified']
    missing_cols = []

    for req_col in required_cols:
        if not any(col['name'] == req_col for col in columns):
            missing_cols.append(req_col)

    return missing_cols


def run_migrations():
    """Run alembic migrations to update the database schema"""
    print("Checking current database schema...")

    missing_columns = check_current_schema()

    if not missing_columns:
        print("All required columns are present in the database. No migration needed.")
        return

    print(f"Missing columns: {missing_columns}")
    print("Running migrations to update the database schema...")

    # Set up alembic config
    alembic_cfg = Config("alembic.ini")

    # Set the database URL for alembic
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    # Run the migrations
    try:
        # Upgrade to the latest version
        command.upgrade(alembic_cfg, "head")
        print("Database migrations completed successfully!")

        # Verify the schema again
        missing_after = check_current_schema()
        if missing_after:
            print(f"Warning: Some columns are still missing after migration: {missing_after}")
        else:
            print("All required columns are now present in the database.")

    except Exception as e:
        print(f"Error running migrations: {e}")
        raise


if __name__ == "__main__":
    run_migrations()