"""empty message

Revision ID: 8ab5f0addef2
Revises: 9a4d79bbeaeb
Create Date: 2023-12-06 19:07:36.858554

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8ab5f0addef2'
down_revision = '9a4d79bbeaeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=20), nullable=False),
                    sa.Column('email', sa.String(length=120), nullable=False),
                    sa.Column('image_file', sa.String(length=20), nullable=False),
                    sa.Column('password', sa.String(length=60), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
