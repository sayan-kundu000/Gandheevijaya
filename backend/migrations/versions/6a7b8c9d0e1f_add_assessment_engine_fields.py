"""add_assessment_engine_fields

Revision ID: 6a7b8c9d0e1f
Revises: 5f6a7b8c9d0e
Create Date: 2026-08-14 15:54:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '6a7b8c9d0e1f'
down_revision: Union[str, Sequence[str], None] = '5f6a7b8c9d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def add_column_if_not_exists(table_name: str, column: sa.Column):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    if column.name not in columns:
        op.add_column(table_name, column)


def upgrade() -> None:
    # Quizzes
    add_column_if_not_exists('quizzes', sa.Column('exam_id', sa.Integer(), nullable=True))
    add_column_if_not_exists('quizzes', sa.Column('topic_id', sa.Integer(), nullable=True))
    add_column_if_not_exists('quizzes', sa.Column('quiz_type', sa.String(length=50), nullable=False, server_default='PRACTICE'))
    add_column_if_not_exists('quizzes', sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'))
    add_column_if_not_exists('quizzes', sa.Column('question_count', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('quizzes', sa.Column('negative_marking', sa.Float(), nullable=False, server_default='0.25'))
    add_column_if_not_exists('quizzes', sa.Column('randomize_questions', sa.Boolean(), nullable=False, server_default='1'))
    add_column_if_not_exists('quizzes', sa.Column('randomize_options', sa.Boolean(), nullable=False, server_default='0'))
    add_column_if_not_exists('quizzes', sa.Column('show_solutions_after_submit', sa.Boolean(), nullable=False, server_default='1'))
    add_column_if_not_exists('quizzes', sa.Column('max_attempts', sa.Integer(), nullable=True))
    add_column_if_not_exists('quizzes', sa.Column('created_by', sa.String(length=36), nullable=True))
    add_column_if_not_exists('quizzes', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Attempts
    add_column_if_not_exists('attempts', sa.Column('total_questions', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('attempted_count', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('correct_count', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('incorrect_count', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('unanswered_count', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('total_marks', sa.Float(), nullable=False, server_default='0.0'))
    add_column_if_not_exists('attempts', sa.Column('percentage', sa.Float(), nullable=False, server_default='0.0'))
    add_column_if_not_exists('attempts', sa.Column('accuracy', sa.Float(), nullable=False, server_default='0.0'))
    add_column_if_not_exists('attempts', sa.Column('time_taken_seconds', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempts', sa.Column('question_order', sa.JSON(), nullable=True))
    add_column_if_not_exists('attempts', sa.Column('option_mappings', sa.JSON(), nullable=True))

    # Attempt Answers
    add_column_if_not_exists('attempt_answers', sa.Column('penalty_deducted', sa.Float(), nullable=False, server_default='0.0'))
    add_column_if_not_exists('attempt_answers', sa.Column('marked_for_review', sa.Boolean(), nullable=False, server_default='0'))
    add_column_if_not_exists('attempt_answers', sa.Column('answered_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))


def downgrade() -> None:
    pass
