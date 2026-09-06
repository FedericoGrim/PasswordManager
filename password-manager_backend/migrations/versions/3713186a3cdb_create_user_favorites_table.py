"""create user favorites table

Revision ID: 3713186a3cdb
Revises: a370b97d32ae
Create Date: 2026-09-02 17:42:15.262557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3713186a3cdb'
down_revision: Union[str, None] = 'a370b97d32ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_favorites',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('sub_account_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sub_account_id'], ['sub_accounts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'sub_account_id', name='uq_user_favorites_user_id_sub_account_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_favorites')
