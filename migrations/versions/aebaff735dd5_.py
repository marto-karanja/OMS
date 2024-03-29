"""empty message

Revision ID: aebaff735dd5
Revises: dfddd4952f35
Create Date: 2022-08-23 12:13:30.613685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aebaff735dd5'
down_revision = 'dfddd4952f35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('thread_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=1000), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('sent_to', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN', name='department'), nullable=True),
    sa.Column('sent_from', sa.Enum('EDITOR', 'FINANCE', 'QUALITY', 'CUSTOMER', 'WRITER', 'ADMIN', name='department'), nullable=True),
    sa.Column('thread_status', sa.Enum('PARENT', 'CHILD', 'DELETED', name='threadstatus'), server_default='CHILD', nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_order_id'), 'messages', ['order_id'], unique=False)
    op.create_index(op.f('ix_messages_recipient_id'), 'messages', ['recipient_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)
    op.create_index(op.f('ix_messages_sent_from'), 'messages', ['sent_from'], unique=False)
    op.create_index(op.f('ix_messages_sent_to'), 'messages', ['sent_to'], unique=False)
    op.create_index(op.f('ix_messages_thread_id'), 'messages', ['thread_id'], unique=False)
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_index(op.f('ix_messages_thread_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_sent_to'), table_name='messages')
    op.drop_index(op.f('ix_messages_sent_from'), table_name='messages')
    op.drop_index(op.f('ix_messages_sender_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_recipient_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_order_id'), table_name='messages')
    op.drop_table('messages')
    # ### end Alembic commands ###
