"""add total column to orders

Revision ID: 443a501b2981
Revises: 2db66aa9a427
Create Date: 2024-01-20 23:37:17.581213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "443a501b2981"
down_revision = "2db66aa9a427"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("total", sa.DECIMAL(precision=12, scale=2), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.drop_column("total")

    # ### end Alembic commands ###
