"""create interview engine tables

Revision ID: 20261007_0003
Revises: 20261007_0002
Create Date: 2026-10-07
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261007_0003"
down_revision: str | None = "20261007_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "question_bank",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("role", sa.String(length=120), nullable=False),
        sa.Column("interview_type", sa.String(length=40), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("topic", sa.String(length=120), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("concepts", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_question_bank_lookup", "question_bank", ["role", "interview_type", "difficulty"])

    op.create_table(
        "interviews",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("resume_id", sa.String(length=36), sa.ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("role", sa.String(length=120), nullable=False),
        sa.Column("interview_type", sa.String(length=40), nullable=False),
        sa.Column("starting_difficulty", sa.String(length=20), nullable=False),
        sa.Column("current_difficulty", sa.String(length=20), nullable=False),
        sa.Column("target_question_count", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_interviews_user_id", "interviews", ["user_id"])
    op.create_index("ix_interviews_user_created", "interviews", ["user_id", "created_at"])

    op.create_table(
        "interview_questions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("interview_id", sa.String(length=36), sa.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(length=120), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("question_type", sa.String(length=40), nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("question_bank_id", sa.String(length=36), sa.ForeignKey("question_bank.id", ondelete="SET NULL"), nullable=True),
        sa.Column("follow_up_of", sa.String(length=36), sa.ForeignKey("interview_questions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("concepts", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_interview_questions_interview_id", "interview_questions", ["interview_id"])
    op.create_index("ix_interview_questions_interview_position", "interview_questions", ["interview_id", "position"])

    op.create_table(
        "interview_answers",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("question_id", sa.String(length=36), sa.ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("word_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_interview_answers_question_id", "interview_answers", ["question_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_interview_answers_question_id", table_name="interview_answers")
    op.drop_table("interview_answers")
    op.drop_index("ix_interview_questions_interview_position", table_name="interview_questions")
    op.drop_index("ix_interview_questions_interview_id", table_name="interview_questions")
    op.drop_table("interview_questions")
    op.drop_index("ix_interviews_user_created", table_name="interviews")
    op.drop_index("ix_interviews_user_id", table_name="interviews")
    op.drop_table("interviews")
    op.drop_index("ix_question_bank_lookup", table_name="question_bank")
    op.drop_table("question_bank")
