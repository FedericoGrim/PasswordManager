"""rename encrypted fields and schema cleanup

Revision ID: a89aea366155
Revises: 300f44a4afd8
Create Date: 2026-08-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a89aea366155'
down_revision: Union[str, None] = '300f44a4afd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'id_keycloak', new_column_name='keycloak_id')
    op.alter_column('sub_accounts', 'username', new_column_name='username_encrypted')
    op.alter_column('sub_accounts', 'email', new_column_name='email_encrypted')
    op.alter_column('sub_accounts', 'password', new_column_name='password_encrypted')
    op.alter_column('sub_accounts', 'link', new_column_name='site_link_encrypted')
    op.alter_column('user_teams_keys', 'key', new_column_name='team_key_encrypted')

    op.drop_column('sub_accounts', 'title')
    op.drop_column('teams', 'salt_argon')

    op.add_column('teams', sa.Column('is_personal', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.alter_column('teams', 'is_personal', server_default=None)

    op.create_unique_constraint('uq_team_members_team_id_user_id', 'team_members', ['team_id', 'user_id'])
    op.create_unique_constraint('uq_categories_team_id_name', 'categories', ['team_id', 'name'])
    op.create_unique_constraint('uq_sub_account_categories_sub_account_id_category_id', 'sub_account_categories', ['sub_account_id', 'category_id'])
    op.create_unique_constraint('uq_user_teams_keys_team_id_user_id', 'user_teams_keys', ['team_id', 'user_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_user_teams_keys_team_id_user_id', 'user_teams_keys', type_='unique')
    op.drop_constraint('uq_sub_account_categories_sub_account_id_category_id', 'sub_account_categories', type_='unique')
    op.drop_constraint('uq_categories_team_id_name', 'categories', type_='unique')
    op.drop_constraint('uq_team_members_team_id_user_id', 'team_members', type_='unique')

    op.drop_column('teams', 'is_personal')

    op.add_column('teams', sa.Column('salt_argon', sa.String(), nullable=False, server_default=''))
    op.alter_column('teams', 'salt_argon', server_default=None)
    op.add_column('sub_accounts', sa.Column('title', sa.String(length=100), nullable=False, server_default=''))
    op.alter_column('sub_accounts', 'title', server_default=None)

    op.alter_column('user_teams_keys', 'team_key_encrypted', new_column_name='key')
    op.alter_column('sub_accounts', 'site_link_encrypted', new_column_name='link')
    op.alter_column('sub_accounts', 'password_encrypted', new_column_name='password')
    op.alter_column('sub_accounts', 'email_encrypted', new_column_name='email')
    op.alter_column('sub_accounts', 'username_encrypted', new_column_name='username')
    op.alter_column('users', 'keycloak_id', new_column_name='id_keycloak')
