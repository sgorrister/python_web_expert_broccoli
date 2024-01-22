"""empty message

Revision ID: fd2335a81fd3
Revises: ba32511068fc
Create Date: 2023-12-20 21:19:22.384163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd2335a81fd3'
down_revision = 'ba32511068fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dwelling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dwelling')
    # ### end Alembic commands ###