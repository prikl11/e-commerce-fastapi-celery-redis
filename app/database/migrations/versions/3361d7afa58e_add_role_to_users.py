"""add role to users

Revision ID: 3361d7afa58e
Revises: 46f81df0b755
Create Date: 2026-07-31 12:50:05.043250

"""
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3361d7afa58e'
down_revision: Union[str, Sequence[str], None] = '46f81df0b755'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    userrole_enum = postgresql.ENUM("customer", "manager", "admin", name="userrole")
    userrole_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            userrole_enum,
            server_default="customer",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
    postgresql.ENUM(name="userrole").drop(op.get_bind(), checkfirst=True)