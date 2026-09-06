"""drop unique constraint on teams name

Revision ID: a370b97d32ae
Revises: ca436cd1e7a2
Create Date: 2026-09-02 15:49:14.112498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a370b97d32ae'
down_revision: Union[str, None] = 'ca436cd1e7a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('teams_name_key', 'teams', type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint('teams_name_key', 'teams', ['name'])
