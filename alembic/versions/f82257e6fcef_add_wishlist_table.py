"""add wishlist table

Revision ID: f82257e6fcef
Revises: 7e8ac1b5497c
Create Date: 2026-10-07 09:15:21.654000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f82257e6fcef'
down_revision: Union[str, Sequence[str], None] = '7e8ac1b5497c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "wishlists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"]
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "customer_id",
            "product_id",
            name="uq_customer_product_wishlist"
        )
    )

    op.create_index(
        op.f("ix_wishlists_id"),
        "wishlists",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_wishlists_id"),
        table_name="wishlists"
    )
    op.drop_table("wishlists")