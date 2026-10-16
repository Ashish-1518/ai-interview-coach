import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.prompts import QUESTION_SYSTEM_PROMPT, build_question_prompt
from app.ai.schemas import GeneratedQuestion, LLMProvider
from app.ai.provider import AIProviderError
from app.models.interview import Interview, InterviewQuestion
from app.models.question_bank import QuestionBankItem

logger = logging.getLogger(__name__)


def find_bank_question(
    db: Session,
    role: str,
    interview_type: str,
    difficulty: str,
    used_bank_ids: set[str],
) -> QuestionBankItem | None:
    """Retrieve the first unused bank question matching the interview context."""

    statement = (
        select(QuestionBankItem)
        .where(
            QuestionBankItem.role == role,
            QuestionBankItem.interview_type == interview_type,
            QuestionBankItem.difficulty == difficulty,
        )
        .order_by(QuestionBankItem.created_at)
    )
    for item in db.scalars(statement):
        if item.id not in used_bank_ids:
            return item
    return None


def build_next_question(
    db: Session,
    interview: Interview,
    provider: LLMProvider | None,
) -> InterviewQuestion:
    """Select the next question: bank first, then LLM generation when configured."""

    asked_prompts = [question.prompt for question in interview.questions]
    used_bank_ids = {question.question_bank_id for question in interview.questions if question.question_bank_id}
    position = len(interview.questions) + 1

    bank_item = find_bank_question(
        db,
        interview.role,
        interview.interview_type,
        interview.current_difficulty,
        used_bank_ids,
    )
    if bank_item is not None:
        return InterviewQuestion(
            interview_id=interview.id,
            position=position,
            prompt=bank_item.prompt,
            topic=bank_item.topic,
            difficulty=bank_item.difficulty,
            question_type=interview.interview_type,
            source="bank",
            question_bank_id=bank_item.id,
            concepts=bank_item.concepts,
        )

    if provider is None:
        raise NoQuestionAvailableError(
            "No question bank entry matches this interview configuration and no AI provider is configured."
        )

    try:
        generated = provider.generate_json(
            QUESTION_SYSTEM_PROMPT,
            build_question_prompt(
                interview.role,
                interview.interview_type,
                interview.current_difficulty,
                asked_prompts,
            ),
            GeneratedQuestion,
        )
    except AIProviderError as exc:
        raise NoQuestionAvailableError("Question generation failed.") from exc

    assert isinstance(generated, GeneratedQuestion)
    return InterviewQuestion(
        interview_id=interview.id,
        position=position,
        prompt=generated.prompt,
        topic=generated.topic,
        difficulty=generated.difficulty,
        question_type=interview.interview_type,
        source="generated",
        question_bank_id=None,
        concepts=generated.concepts,
    )


class NoQuestionAvailableError(Exception):
    """Raised when neither the question bank nor an LLM can supply a question."""
