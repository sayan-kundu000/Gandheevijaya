"""add_attempt_unique_constraint

Revision ID: 7b8c9d0e1f2a
Revises: 6a7b8c9d0e1f
Create Date: 2026-08-14 16:13:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8c9d0e1f2a'
down_revision: Union[str, None] = '6a7b8c9d0e1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch_alter_table for SQLite & PostgreSQL compatibility
    with op.batch_alter_table('attempt_answers') as batch_op:
        batch_op.create_unique_constraint(
            'uq_attempt_question_answer',
            ['attempt_id', 'question_id']
        )
    with op.batch_alter_table('attempts') as batch_op:
        batch_op.create_index(
            'idx_attempts_user_quiz_status',
            ['user_id', 'quiz_id', 'status']
        )


def downgrade() -> None:
    with op.batch_alter_table('attempts') as batch_op:
        batch_op.drop_index('idx_attempts_user_quiz_status')
    with op.batch_alter_table('attempt_answers') as batch_op:
        batch_op.drop_constraint('uq_attempt_question_answer', type_='unique')
