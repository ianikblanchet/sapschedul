"""avec cap

Revision ID: 8c60426d0de3
Revises: 764711ca7ca0
Create Date: 2022-02-04 08:32:39.214544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c60426d0de3'
down_revision = '764711ca7ca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('capac', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cap', sa.Float(), nullable=True))
        batch_op.create_index(batch_op.f('ix_capac_cap'), ['cap'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('capac', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_capac_cap'))
        batch_op.drop_column('cap')

    # ### end Alembic commands ###
