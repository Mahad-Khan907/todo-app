"""Add recurring and reminder fields

Revision ID: 20260131_add_recurring_and_reminder_fields
Revises:
Create Date: 2026-01-31 23:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '20260131_add_recurring_and_reminder_fields'
down_revision: Union[str, None] = '17e8115a0cf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns for recurring tasks
    op.add_column('task', sa.Column('is_recurring', sa.Boolean(), nullable=False, default=False))
    op.add_column('task', sa.Column('recurring_pattern', sa.String(), nullable=True))

    # Add columns for reminders
    op.add_column('task', sa.Column('reminder_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('task', sa.Column('last_notified', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Remove columns for recurring tasks
    op.drop_column('task', 'last_notified')
    op.drop_column('task', 'reminder_at')
    op.drop_column('task', 'recurring_pattern')
    op.drop_column('task', 'is_recurring')