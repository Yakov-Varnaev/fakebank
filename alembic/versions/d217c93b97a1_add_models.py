"""add_models

Revision ID: d217c93b97a1
Revises: 
Create Date: 2024-02-25 20:44:34.992930

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd217c93b97a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table(
        'account',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('balance', sa.DECIMAL(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'],),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'transaction',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sent_from', sa.UUID(), nullable=False),
        sa.Column('sent_to', sa.UUID(), nullable=False),
        sa.Column('amount', sa.DECIMAL(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.CheckConstraint('amount > 0'),
        sa.CheckConstraint('sent_from != sent_to'),
        sa.ForeignKeyConstraint(['sent_from'], ['account.id'],),
        sa.ForeignKeyConstraint(['sent_to'], ['account.id'],),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('account')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
