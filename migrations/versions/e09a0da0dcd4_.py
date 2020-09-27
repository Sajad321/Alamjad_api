"""empty message

Revision ID: e09a0da0dcd4
Revises: 1000c08fda3a
Create Date: 2020-09-25 17:00:39.398491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e09a0da0dcd4'
down_revision = '1000c08fda3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctor', sa.Column(
        'report_activity', sa.Boolean(), nullable=True))
    op.add_column('pharmacy', sa.Column(
        'order_activity', sa.Boolean(), nullable=True))
    # op.create_foreign_key(None, 'report', 'availability_of_item', ['availability_of_item_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'report', type_='foreignkey')
    op.drop_column('pharmacy', 'order_activity')
    op.drop_column('doctor', 'report_activity')
    # ### end Alembic commands ###
