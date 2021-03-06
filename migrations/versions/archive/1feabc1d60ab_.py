"""empty message

Revision ID: 1feabc1d60ab
Revises: 3b8806ab93c8
Create Date: 2022-04-19 15:10:36.195457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1feabc1d60ab'
down_revision = '3b8806ab93c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('department', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', name='department'), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=1000), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_table('messages')
    # ### end Alembic commands ###
