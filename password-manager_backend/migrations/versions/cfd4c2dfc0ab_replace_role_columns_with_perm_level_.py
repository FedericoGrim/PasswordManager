"""replace role columns with perm level fk

Revision ID: cfd4c2dfc0ab
Revises: b8087235009f
Create Date: 2026-08-14 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfd4c2dfc0ab'
down_revision: Union[str, None] = 'b8087235009f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    NOTE: perm_level_id/required_perm_level_id are added as NOT NULL with no
    default. This will fail if team_members/sub_accounts already have rows in
    the target database - acceptable here since this is a dev database with
    no data to preserve.
    """
    op.drop_column('team_members', 'role')
    op.add_column('team_members', sa.Column('perm_level_id', sa.UUID(), nullable=False))
    op.create_foreign_key('fk_team_members_perm_level_id_team_perm_levels', 'team_members', 'team_perm_levels', ['perm_level_id'], ['id'], ondelete='CASCADE')

    op.drop_column('sub_accounts', 'necessary_role')
    op.add_column('sub_accounts', sa.Column('required_perm_level_id', sa.UUID(), nullable=False))
    op.create_foreign_key('fk_sub_accounts_required_perm_level_id_team_perm_levels', 'sub_accounts', 'team_perm_levels', ['required_perm_level_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_sub_accounts_required_perm_level_id_team_perm_levels', 'sub_accounts', type_='foreignkey')
    op.drop_column('sub_accounts', 'required_perm_level_id')
    op.add_column('sub_accounts', sa.Column('necessary_role', sa.String(length=50), nullable=False, server_default=''))
    op.alter_column('sub_accounts', 'necessary_role', server_default=None)

    op.drop_constraint('fk_team_members_perm_level_id_team_perm_levels', 'team_members', type_='foreignkey')
    op.drop_column('team_members', 'perm_level_id')
    op.add_column('team_members', sa.Column('role', sa.String(length=50), nullable=False, server_default=''))
    op.alter_column('team_members', 'role', server_default=None)
