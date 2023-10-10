"""empty message

Revision ID: b44c19fec958
Revises: 77155f2a8fec
Create Date: 2023-10-09 17:56:57.062946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b44c19fec958'
down_revision: Union[str, None] = '77155f2a8fec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
