"""empty message

Revision ID: cdf2533fad1c
Revises: fde8ad6b2f1d
Create Date: 2022-08-28 13:37:09.944234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdf2533fad1c'
down_revision = 'fde8ad6b2f1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_image_path', sa.String(length=1000), nullable=True))
    op.add_column('user', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('ranking', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('education_level', sa.Enum('HIGH_SCHOOL', 'UNDERGRADUATE', 'DIPLOMA', 'CERTIFICATE', name='educationlevel'), nullable=True))
    op.add_column('user', sa.Column('certificate_path', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'certificate_path')
    op.drop_column('user', 'education_level')
    op.drop_column('user', 'ranking')
    op.drop_column('user', 'about_me')
    op.drop_column('user', 'profile_image_path')
    # ### end Alembic commands ###