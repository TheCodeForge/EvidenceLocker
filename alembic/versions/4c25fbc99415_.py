"""empty message

Revision ID: 4c25fbc99415
Revises: 9eb2d755a8a1
Create Date: 2022-07-18 14:12:40.748524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c25fbc99415'
down_revision = '9eb2d755a8a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('image_type', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entries', 'image_type')
    # ### end Alembic commands ###
