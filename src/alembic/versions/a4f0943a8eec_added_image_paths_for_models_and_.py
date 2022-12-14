"""added image paths for models and datasets

Revision ID: a4f0943a8eec
Revises: 5a1457d50acc
Create Date: 2022-03-25 09:11:09.930877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4f0943a8eec'
down_revision = '5a1457d50acc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('datasets', sa.Column('img_path', sa.String(), nullable=True))
    op.add_column('models', sa.Column('img_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('models', 'img_path')
    op.drop_column('datasets', 'img_path')
    # ### end Alembic commands ###
