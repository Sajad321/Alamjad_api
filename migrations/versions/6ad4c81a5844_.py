"""empty message

Revision ID: 6ad4c81a5844
Revises: aaf374d23edd
Create Date: 2020-08-30 18:25:05.291933

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6ad4c81a5844'
down_revision = 'aaf374d23edd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('notification_ibfk_1', 'notification', type_='foreignkey')
    op.drop_column('notification', 'order_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('order_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('notification_ibfk_1', 'notification', 'order', ['order_id'], ['id'])
    # ### end Alembic commands ###