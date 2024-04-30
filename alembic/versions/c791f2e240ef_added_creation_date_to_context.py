"""added creation date to context

Revision ID: c791f2e240ef
Revises: e67742358865
Create Date: 2023-09-29 07:57:06.812261

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c791f2e240ef'
down_revision: Union[str, None] = 'e67742358865'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('contexts', sa.Column('creation_date', sa.DateTime(), default=datetime.datetime.utcnow))


def downgrade() -> None:
    op.drop_column('contexts', 'creation_date')
