"""create team perm levels table

Revision ID: b8087235009f
Revises: a89aea366155
Create Date: 2026-08-14 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8087235009f'
down_revision: Union[str, None] = 'a89aea366155'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('team_perm_levels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('team_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('team_id', 'name', name='uq_team_perm_levels_team_id_name')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('team_perm_levels')
