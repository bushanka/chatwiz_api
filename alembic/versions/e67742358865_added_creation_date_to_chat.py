"""added creation date to chat

Revision ID: e67742358865
Revises: f38bac51634e
Create Date: 2023-09-29 05:57:36.640095

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e67742358865'
down_revision: Union[str, None] = 'f38bac51634e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chats', sa.Column('creation_date', sa.DateTime(), default=datetime.datetime.utcnow))


def downgrade() -> None:
    op.drop_column('chats', 'creation_date')