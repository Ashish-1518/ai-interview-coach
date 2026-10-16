"""create answer evaluations table

Revision ID: 20261007_0004
Revises: 20261007_0003
Create Date: 2026-10-07
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261007_0004"
down_revision: str | None = "20261007_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "answer_evaluations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("answer_id", sa.String(length=36), sa.ForeignKey("interview_answers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
        sa.Column("technical_accuracy_score", sa.Float(), nullable=True),
        sa.Column("completeness_score", sa.Float(), nullable=True),
        sa.Column("communication_score", sa.Float(), nullable=True),
        sa.Column("structure_score", sa.Float(), nullable=True),
        sa.Column("specificity_score", sa.Float(), nullable=True),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("weaknesses", sa.JSON(), nullable=False),
        sa.Column("suggestions", sa.JSON(), nullable=False),
        sa.Column("star_evaluation", sa.JSON(), nullable=True),
        sa.Column("text_features", sa.JSON(), nullable=False),
        sa.Column("method_map", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_answer_evaluations_answer_id", "answer_evaluations", ["answer_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_answer_evaluations_answer_id", table_name="answer_evaluations")
    op.drop_table("answer_evaluations")
