"""empty message

Revision ID: 819dc2158929
Revises: d4399cab4a40
Create Date: 2023-12-10 00:33:16.077265

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '819dc2158929'
down_revision = 'd4399cab4a40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=20), server_default='default.jpg', nullable=False))
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')
        batch_op.drop_column('image_file')

    # ### end Alembic commands ###
