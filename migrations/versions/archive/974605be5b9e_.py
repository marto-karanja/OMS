"""empty message

Revision ID: 974605be5b9e
Revises: 70e2bfc5a409
Create Date: 2022-03-20 22:40:10.390836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '974605be5b9e'
down_revision = '70e2bfc5a409'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_message_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_message_read_time')
    # ### end Alembic commands ###
