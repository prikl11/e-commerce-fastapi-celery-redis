"""add search_vector to products

Revision ID: 85cf101c8fbf
Revises: c47ff2daf174
Create Date: 2026-07-30 16:41:20.990233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR


# revision identifiers, used by Alembic.
revision: str = '85cf101c8fbf'
down_revision: Union[str, Sequence[str], None] = 'c47ff2daf174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("products", sa.Column("search_vector", TSVECTOR, nullable=True))
    op.execute("""
        CREATE INDEX ix_products_search_vector
        ON products USING GIN (search_vector)
    """)

def downgrade():
    op.execute("DROP INDEX ix_products_search_vector")
    op.drop_column("products", "search_vector")