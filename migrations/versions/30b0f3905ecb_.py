"""empty message

Revision ID: 30b0f3905ecb
Revises: a8711e0550fb
Create Date: 2020-08-27 12:21:11.680459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '30b0f3905ecb'
down_revision = 'a8711e0550fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('doctor', 'loyality')
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
    op.add_column('doctor', sa.Column('loyality', mysql.VARCHAR(length=200), nullable=False))
    # ### end Alembic commands ###