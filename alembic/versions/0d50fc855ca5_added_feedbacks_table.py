"""added_feedbacks_table

Revision ID: 0d50fc855ca5
Revises: c791f2e240ef
Create Date: 2023-09-30 15:08:57.488115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d50fc855ca5'
down_revision: Union[str, None] = 'c791f2e240ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'feedbacks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('comment_text', sa.String(255), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('feedbacks')
