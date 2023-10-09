"""empty message

Revision ID: 77155f2a8fec
Revises: 749b31f5098e
Create Date: 2023-10-09 20:33:56.195674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77155f2a8fec'
down_revision: Union[str, None] = '749b31f5098e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
