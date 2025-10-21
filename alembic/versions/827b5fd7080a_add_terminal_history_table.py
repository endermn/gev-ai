"""add_terminal_history_table

Revision ID: 827b5fd7080a
Revises: 5c1fe0bf3b90
Create Date: 2025-10-21 08:02:22.312670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '827b5fd7080a'
down_revision: Union[str, Sequence[str], None] = '5c1fe0bf3b90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'terminal_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('command', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('embedding', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_terminal_history_id'), 'terminal_history', ['id'], unique=False)
    op.create_index(op.f('ix_terminal_history_command'), 'terminal_history', ['command'], unique=False)
    op.create_index(op.f('ix_terminal_history_timestamp'), 'terminal_history', ['timestamp'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_terminal_history_timestamp'), table_name='terminal_history')
    op.drop_index(op.f('ix_terminal_history_command'), table_name='terminal_history')
    op.drop_index(op.f('ix_terminal_history_id'), table_name='terminal_history')
    op.drop_table('terminal_history')
