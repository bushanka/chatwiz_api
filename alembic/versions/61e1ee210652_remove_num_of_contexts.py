"""remove_num_of_contexts

Revision ID: 61e1ee210652
Revises: d85b3bffde3a
Create Date: 2023-10-14 20:05:03.483662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '61e1ee210652'
down_revision: Union[str, None] = 'd85b3bffde3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'num_of_contexts')


def downgrade() -> None:
    op.add_column('users', sa.Column('num_of_contexts', sa.INTEGER(), autoincrement=False, default=0))
