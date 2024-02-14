"""add_account_model

Revision ID: aa33233d2848
Revises: a8e6b2985249
Create Date: 2024-02-14 20:06:45.970177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision: str = 'aa33233d2848'
down_revision: Union[str, None] = 'a8e6b2985249'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'account',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column(
            'user_id',
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=True,
        ),
        sa.Column('balance', sa.DECIMAL(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'],),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    # ### end Alembic commands ###