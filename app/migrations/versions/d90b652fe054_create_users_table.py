"""create users table

Revision ID: d90b652fe054
Revises: 
Create Date: 2024-11-13 20:07:05.476403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd90b652fe054'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=31), nullable=False),
    sa.Column('last_name', sa.String(length=31), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=60), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
