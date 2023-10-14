"""add_max_action_points_number

Revision ID: d85b3bffde3a
Revises: 0d50fc855ca5
Create Date: 2023-10-13 20:26:33.703384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd85b3bffde3a'
down_revision: Union[str, None] = '0d50fc855ca5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('subscription_plan', sa.Column('max_action_points', sa.Integer, default=0))
    op.alter_column('users', 'num_of_requests_used', new_column_name='action_points_used')


def downgrade() -> None:
    op.drop_column('subscription_plan', 'max_action_points')
    op.alter_column('users', 'action_points_used', new_column_name='num_of_requests_used')
