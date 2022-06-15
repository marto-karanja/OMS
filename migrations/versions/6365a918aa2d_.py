"""empty message

Revision ID: 6365a918aa2d
Revises: dd3de8e9d3ac
Create Date: 2022-05-21 18:19:45.051710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6365a918aa2d'
down_revision = 'dd3de8e9d3ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('paper_length', sa.Numeric(precision=65, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'paper_length')
    # ### end Alembic commands ###
