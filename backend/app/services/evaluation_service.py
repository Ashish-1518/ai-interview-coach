import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.evaluation import (
    EVALUATION_SYSTEM_PROMPT,
    STAR_EVALUATION_SYSTEM_PROMPT,
    LLMEvaluationResult,
    STAREvaluationResult,
    build_evaluation_prompt,
)
from app.ai.provider import AIProviderError
from app.ai.schemas import LLMProvider
from app.models.evaluation import AnswerEvaluation
from app.models.interview import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.nlp.text_features import TextFeatures, extract_text_features
from app.schemas.answer import AnswerSubmit

logger = logging.getLogger(__name__)


class AnswerAlreadyExistsError(Exception):
    """Raised when an answer has already been submitted for this question."""


def submit_and_evaluate(
    db: Session,
    question: InterviewQuestion,
    answer_in: AnswerSubmit,
    provider: LLMProvider | None,
) -> tuple[InterviewAnswer, AnswerEvaluation]:
    """Save the answer first, then evaluate. A failed evaluation never loses the answer."""

    existing = db.scalar(select(InterviewAnswer).where(InterviewAnswer.question_id == question.id))
    if existing is not None:
        raise AnswerAlreadyExistsError("An answer has already been submitted for this question.")

    words = answer_in.content.split()
    answer = InterviewAnswer(
        question_id=question.id,
        content=answer_in.content,
        word_count=len(words),
    )
    db.add(answer)
    db.flush()

    text_features = extract_text_features(answer_in.content)
    method_map: dict[str, str] = {"text_features": "nlp:deterministic"}

    llm_result: LLMEvaluationResult | None = None
    star_result: STAREvaluationResult | None = None

    if provider is not None:
        llm_result = _try_llm_evaluation(provider, question.prompt, answer_in.content)
        if llm_result is not None:
            for field in ("overall_score", "relevance", "technical_accuracy", "completeness",
                          "communication", "structure", "specificity"):
                method_map[field] = f"llm:{field}"

        if question.question_type == "behavioral" and provider is not None:
            star_result = _try_star_evaluation(provider, question.prompt, answer_in.content)
            if star_result is not None:
                method_map["star_evaluation"] = "llm:star"

    evaluation = AnswerEvaluation(
        answer_id=answer.id,
        overall_score=llm_result.overall_score if llm_result else None,
        relevance_score=llm_result.relevance if llm_result else None,
        technical_accuracy_score=llm_result.technical_accuracy if llm_result else None,
        completeness_score=llm_result.completeness if llm_result else None,
        communication_score=llm_result.communication if llm_result else None,
        structure_score=llm_result.structure if llm_result else None,
        specificity_score=llm_result.specificity if llm_result else None,
        strengths=llm_result.strengths if llm_result else [],
        weaknesses=llm_result.weaknesses if llm_result else [],
        suggestions=llm_result.suggestions if llm_result else [],
        star_evaluation=star_result.model_dump() if star_result else None,
        text_features=text_features.model_dump(),
        method_map=method_map,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(answer)
    db.refresh(evaluation)
    return answer, evaluation


def _try_llm_evaluation(provider: LLMProvider, question_prompt: str, answer_content: str) -> LLMEvaluationResult | None:
    try:
        result = provider.generate_json(
            EVALUATION_SYSTEM_PROMPT,
            build_evaluation_prompt(question_prompt, answer_content),
            LLMEvaluationResult,
        )
        assert isinstance(result, LLMEvaluationResult)
        return result
    except (AIProviderError, AssertionError) as exc:
        logger.warning("LLM evaluation failed, proceeding with NLP-only results: %s", exc)
        return None


def _try_star_evaluation(provider: LLMProvider, question_prompt: str, answer_content: str) -> STAREvaluationResult | None:
    try:
        result = provider.generate_json(
            STAR_EVALUATION_SYSTEM_PROMPT,
            build_evaluation_prompt(question_prompt, answer_content),
            STAREvaluationResult,
        )
        assert isinstance(result, STAREvaluationResult)
        return result
    except (AIProviderError, AssertionError) as exc:
        logger.warning("STAR evaluation failed: %s", exc)
        return None
