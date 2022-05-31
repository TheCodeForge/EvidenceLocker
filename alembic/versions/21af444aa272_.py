"""empty message

Revision ID: 21af444aa272
Revises: 6e3b2ce4c452
Create Date: 2022-05-31 11:38:56.105558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21af444aa272'
down_revision = '6e3b2ce4c452'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('title', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs', 'title')
    # ### end Alembic commands ###