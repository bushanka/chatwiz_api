"""create_table

Revision ID: d91768060353
Revises: 
Create Date: 2023-08-31 22:45:32.302917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import text

revision: str = 'd91768060353'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('surname', sa.String(255), nullable=False),  # нахуя
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('confirmed_registration', sa.Boolean, nullable=False, server_default=text('false')),
        sa.Column('num_of_contents', sa.Integer, nullable=False, server_default=text('0')),
        sa.Column('num_of_requests_used', sa.Integer, nullable=False, server_default=text('0')),
        sa.Column('subscription_type', sa.Integer, nullable=False),  # todo make it foreign key
    )

    op.create_table(
        'subscription_plan',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('price', sa.Integer, nullable=False),
        sa.Column('max_content_amount', sa.Integer, nullable=False),
        sa.Column('max_content_size', sa.Integer, nullable=False),
        sa.Column('max_question_length', sa.Integer, nullable=False),
    )

    op.create_table(
        'contents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('size', sa.Float, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),  # todo foreign key
        sa.Column('path', sa.String(255), nullable=False),
    )

    op.create_table(
        'chats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),  # todo foreign key
        sa.Column('content_id', sa.Integer, nullable=True),  # todo  foreign key
    )

    op.create_table(
        'user_messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chat_id', sa.Integer, nullable=False),  # todo foreign key
        sa.Column('text', sa.Text, nullable=False),
    )

    op.create_table(
        'answer_messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_message_id', sa.Integer, nullable=False),  # todo foreign key
        sa.Column('text', sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('subscription_plan')
    op.drop_table('contents')
    op.drop_table('chats')
    op.drop_table('user_messages')
    op.drop_table('answer_messages')
