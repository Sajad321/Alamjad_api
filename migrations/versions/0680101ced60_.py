"""empty message

Revision ID: 0680101ced60
Revises: 50b8cdae0e1b
Create Date: 2020-08-29 19:42:28.717517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0680101ced60'
down_revision = '50b8cdae0e1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###