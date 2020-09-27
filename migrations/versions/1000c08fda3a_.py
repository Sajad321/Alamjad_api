"""empty message

Revision ID: 1000c08fda3a
Revises: 19eef85559c6
Create Date: 2020-09-11 22:28:13.167305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1000c08fda3a'
down_revision = '19eef85559c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('doctor_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'doctor', ['doctor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'doctor_id')
    # ### end Alembic commands ###