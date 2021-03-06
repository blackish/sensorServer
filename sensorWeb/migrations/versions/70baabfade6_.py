"""empty message

Revision ID: 70baabfade6
Revises: 21da47678b6
Create Date: 2016-10-29 20:50:56.207352

"""

# revision identifiers, used by Alembic.
revision = '70baabfade6'
down_revision = '21da47678b6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weather', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather')
    ### end Alembic commands ###
