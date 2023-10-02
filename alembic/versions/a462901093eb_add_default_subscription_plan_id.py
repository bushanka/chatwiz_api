"""add_default_subscription_plan_id

Revision ID: a462901093eb
Revises: d91768060353
Create Date: 2023-09-11 21:50:49.314080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import text

revision: str = 'a462901093eb'
down_revision: Union[str, None] = 'd91768060353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'subscription_type', server_default=text('1'))
    op.alter_column('users',
                    'subscription_type',
                    new_column_name='subscription_plan_id')


def downgrade() -> None:
    op.alter_column('users', 'subscription_type', server_default=None)
    op.alter_column('users',
                    'subscription_plan_id',
                    new_column_name='subscription_type')
