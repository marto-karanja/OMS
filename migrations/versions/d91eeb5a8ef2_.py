"""empty message

Revision ID: d91eeb5a8ef2
Revises: 0f810d150e8e
Create Date: 2022-06-05 02:53:05.201369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd91eeb5a8ef2'
down_revision = '0f810d150e8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'description')
    # ### end Alembic commands ###
