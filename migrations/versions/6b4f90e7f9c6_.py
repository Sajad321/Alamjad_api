"""empty message

Revision ID: 6b4f90e7f9c6
Revises: 1f3b75e3b93c
Create Date: 2020-09-11 17:26:13.476025

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6b4f90e7f9c6'
down_revision = '1f3b75e3b93c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column(
        'daily_report', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'daily_report')
    # ### end Alembic commands ###
