"""add user table

Revision ID: d319718a7c17
Revises: 
Create Date: 2024-11-14 11:49:22.287439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd319718a7c17'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hero',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('secret_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hero')
    # ### end Alembic commands ###
