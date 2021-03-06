"""empty message

Revision ID: 9625a57a8208
Revises: a8db2867acc7
Create Date: 2022-05-14 17:57:00.675874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9625a57a8208'
down_revision = 'a8db2867acc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('sent_to', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', name='department'), nullable=True))
    op.add_column('messages', sa.Column('sent_from', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', name='department'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'sent_from')
    op.drop_column('messages', 'sent_to')
    # ### end Alembic commands ###
