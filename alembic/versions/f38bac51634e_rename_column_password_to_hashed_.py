"""rename_column_password_to_hashed_password

Revision ID: f38bac51634e
Revises: a462901093eb
Create Date: 2023-09-15 20:56:57.224231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f38bac51634e'
down_revision: Union[str, None] = 'a462901093eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users',
                    'password',
                    new_column_name='hashed_password')


def downgrade() -> None:
    op.alter_column('users',
                    'hashed_password',
                    new_column_name='password')
