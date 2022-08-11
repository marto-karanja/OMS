"""empty message

Revision ID: 77be64167193
Revises: a067ce6040f0
Create Date: 2022-04-19 13:41:20.199181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77be64167193'
down_revision = 'a067ce6040f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('subject', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'subject')
    # ### end Alembic commands ###