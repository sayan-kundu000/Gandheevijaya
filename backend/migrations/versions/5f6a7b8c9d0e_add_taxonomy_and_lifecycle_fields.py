"""add_taxonomy_and_lifecycle_fields

Revision ID: 5f6a7b8c9d0e
Revises: 4e5f6a7b8c9d
Create Date: 2026-08-14 15:40:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '5f6a7b8c9d0e'
down_revision: Union[str, Sequence[str], None] = '4e5f6a7b8c9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def add_column_if_not_exists(table_name: str, column: sa.Column):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    if column.name not in columns:
        op.add_column(table_name, column)


def upgrade() -> None:
    # Exams
    add_column_if_not_exists('exams', sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'))
    add_column_if_not_exists('exams', sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('exams', sa.Column('created_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))
    add_column_if_not_exists('exams', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Subjects
    add_column_if_not_exists('subjects', sa.Column('description', sa.Text(), nullable=True))
    add_column_if_not_exists('subjects', sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'))
    add_column_if_not_exists('subjects', sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('subjects', sa.Column('created_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))
    add_column_if_not_exists('subjects', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Topics
    add_column_if_not_exists('topics', sa.Column('code', sa.String(length=50), nullable=True))
    add_column_if_not_exists('topics', sa.Column('description', sa.Text(), nullable=True))
    add_column_if_not_exists('topics', sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'))
    add_column_if_not_exists('topics', sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
    add_column_if_not_exists('topics', sa.Column('created_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))
    add_column_if_not_exists('topics', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Subtopics
    add_column_if_not_exists('subtopics', sa.Column('created_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Questions
    add_column_if_not_exists('questions', sa.Column('status', sa.String(length=50), nullable=False, server_default='PUBLISHED'))
    add_column_if_not_exists('questions', sa.Column('created_by', sa.String(length=36), nullable=True))
    add_column_if_not_exists('questions', sa.Column('updated_by', sa.String(length=36), nullable=True))
    add_column_if_not_exists('questions', sa.Column('created_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))
    add_column_if_not_exists('questions', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))

    # Study Materials
    add_column_if_not_exists('study_materials', sa.Column('status', sa.String(length=50), nullable=False, server_default='PUBLISHED'))
    add_column_if_not_exists('study_materials', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='2026-01-01 00:00:00'))


def downgrade() -> None:
    op.drop_column('study_materials', 'updated_at')
    op.drop_column('study_materials', 'status')
    op.drop_column('questions', 'updated_at')
    op.drop_column('questions', 'created_at')
    op.drop_column('questions', 'updated_by')
    op.drop_column('questions', 'created_by')
    op.drop_column('questions', 'status')
    op.drop_column('subtopics', 'created_at')
    op.drop_column('topics', 'updated_at')
    op.drop_column('topics', 'created_at')
    op.drop_column('topics', 'display_order')
    op.drop_column('topics', 'status')
    op.drop_column('topics', 'description')
    op.drop_column('topics', 'code')
    op.drop_column('subjects', 'updated_at')
    op.drop_column('subjects', 'created_at')
    op.drop_column('subjects', 'display_order')
    op.drop_column('subjects', 'status')
    op.drop_column('subjects', 'description')
    op.drop_column('exams', 'updated_at')
    op.drop_column('exams', 'created_at')
    op.drop_column('exams', 'display_order')
    op.drop_column('exams', 'status')
