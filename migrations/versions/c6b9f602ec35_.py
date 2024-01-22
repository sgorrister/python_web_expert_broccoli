"""empty message

Revision ID: c6b9f602ec35
Revises: fd2335a81fd3
Create Date: 2024-01-22 18:48:08.284194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6b9f602ec35'
down_revision = 'fd2335a81fd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Enum('low', 'medium', 'high', name='enumpriority'), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###