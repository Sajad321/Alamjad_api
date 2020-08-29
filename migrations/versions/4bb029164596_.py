"""empty message

Revision ID: 4bb029164596
Revises: 30b0f3905ecb
Create Date: 2020-08-29 10:24:01.790836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bb029164596'
down_revision = '30b0f3905ecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_order', sa.Column('bonus', sa.Integer(), nullable=True))
    op.add_column('item_order', sa.Column('gift', sa.Boolean(), nullable=True))
    op.add_column('report', sa.Column('date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('report', 'date')
    op.drop_column('item_order', 'gift')
    op.drop_column('item_order', 'bonus')
    # ### end Alembic commands ###
