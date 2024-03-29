"""make model id size 32

Revision ID: a94d4c4a12a4
Revises: 02ad9c3b3f4f
Create Date: 2024-01-07 23:09:08.750965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a94d4c4a12a4"
down_revision = "02ad9c3b3f4f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("book", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    with op.batch_alter_table("book_order", schema=None) as batch_op:
        batch_op.alter_column(
            "book_id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "order_id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    with op.batch_alter_table("customer", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    with op.batch_alter_table("image", schema=None) as batch_op:
        batch_op.alter_column(
            "book_id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.alter_column(
            "customer_id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "pickup_location_id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    with op.batch_alter_table("pickup_location", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(length=24),
            type_=sa.String(length=36),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pickup_location", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "pickup_location_id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "customer_id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    with op.batch_alter_table("image", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "book_id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    with op.batch_alter_table("customer", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    with op.batch_alter_table("book_order", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "order_id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "book_id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    with op.batch_alter_table("book", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=36),
            type_=sa.VARCHAR(length=24),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
