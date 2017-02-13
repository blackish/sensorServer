"""empty message

Revision ID: 33c15b049a1c
Revises: None
Create Date: 2016-10-22 18:24:00.147234

"""

# revision identifiers, used by Alembic.
revision = '33c15b049a1c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('configs',
    sa.Column('cname', sa.String(length=128), nullable=False),
    sa.Column('value', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('cname')
    )
    op.create_table('sensor_type',
    sa.Column('sensor_type_id', sa.Integer(), nullable=False),
    sa.Column('sensor_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('sensor_type_id')
    )
    op.create_table('devices',
    sa.Column('address', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('address')
    )
    op.create_table('sensors',
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('sensor_type', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('fix_value', sa.Float(), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.address'], ),
    sa.ForeignKeyConstraint(['sensor_type'], ['sensor_type.sensor_type_id'], ),
    sa.PrimaryKeyConstraint('device_id', 'sensor_type')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensors')
    op.drop_table('devices')
    op.drop_table('sensor_type')
    op.drop_table('configs')
    ### end Alembic commands ###
