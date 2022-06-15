"""empty message

Revision ID: 3b8806ab93c8
Revises: 77be64167193
Create Date: 2022-04-19 14:32:52.362402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8806ab93c8'
down_revision = '77be64167193'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'messages', 'user', ['recipient_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'recipient_id')
    # ### end Alembic commands ###
