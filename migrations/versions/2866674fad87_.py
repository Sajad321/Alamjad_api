"""empty message

Revision ID: 2866674fad87
Revises: 6ad4c81a5844
Create Date: 2020-08-30 21:00:19.248669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2866674fad87'
down_revision = '6ad4c81a5844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'order', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    # ### end Alembic commands ###