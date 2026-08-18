"""add_question_source_fingerprint

Revision ID: 4e5f6a7b8c9d
Revises: 3a4b5c6d7e8f
Create Date: 2026-08-14 15:20:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4e5f6a7b8c9d'
down_revision: Union[str, Sequence[str], None] = '3a4b5c6d7e8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('questions', sa.Column('source_fingerprint', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_questions_source_fingerprint'), 'questions', ['source_fingerprint'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_questions_source_fingerprint'), table_name='questions')
    op.drop_column('questions', 'source_fingerprint')
