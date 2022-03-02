"""empty message

Revision ID: 8445d5b4fff7
Revises: 357eac7c3fff
Create Date: 2022-02-22 14:00:07.206671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8445d5b4fff7'
down_revision = '357eac7c3fff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('victim_users', sa.Column('name', sa.String(length=128), nullable=True))
    op.add_column('victim_users', sa.Column('country', sa.String(length=2), nullable=True))
    op.add_column('victim_users', sa.Column('pw_hash', sa.String(length=256), nullable=True))
    op.add_column('victim_users', sa.Column('otp_secret', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('victim_users', 'otp_secret')
    op.drop_column('victim_users', 'pw_hash')
    op.drop_column('victim_users', 'country')
    op.drop_column('victim_users', 'name')
    # ### end Alembic commands ###