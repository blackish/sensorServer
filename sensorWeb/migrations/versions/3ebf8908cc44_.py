"""empty message

Revision ID: 3ebf8908cc44
Revises: 198b52807527
Create Date: 2016-10-28 23:24:49.970378

"""

# revision identifiers, used by Alembic.
revision = '3ebf8908cc44'
down_revision = '198b52807527'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedulers', sa.Column('descr', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedulers', 'descr')
    ### end Alembic commands ###
