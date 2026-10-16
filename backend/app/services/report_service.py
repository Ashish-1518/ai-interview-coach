"""
Report and analytics service — builds aggregated views from raw data.

KEY DESIGN CHOICES (for your viva):

1. All maths here is plain Python (sum, mean, Counter). No numpy or pandas —
   they'd be overkill for small lists and add huge install size.

2. The "strongest / weakest topics" ranking is computed by grouping all scored
   evaluations by their question's topic and sorting by average score. This is
   a real calculation, not a guess.

3. `score_trend` is the chronological list of average-overall-scores per
   interview. Frontend can plot this directly as a line chart.
"""
from collections import Counter, defaultdict

from sqlalchemy.orm import Session, selectinload

from app.models.evaluation import AnswerEvaluation
from app.models.interview import Interview, InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.models.user import User
from app.schemas.evaluation import EvaluationResponse
from app.schemas.interview import InterviewResponse, QuestionResponse
from app.schemas.report import (
    AnalyticsSummaryResponse,
    InterviewHistoryItem,
    InterviewReportResponse,
    QuestionReportItem,
    ReportSummary,
)


# ---------------------------------------------------------------------------
# Single interview report
# ---------------------------------------------------------------------------

def build_interview_report(db: Session, interview: Interview) -> InterviewReportResponse:
    """Build a full report for one interview, including all Q/A/evaluation data.

    Uses eager loading to fetch questions → answers → evaluations in one round
    trip instead of N+1 queries.
    """
    # Re-query with eager loads
    interview = db.get(
        Interview,
        interview.id,
        options=[
            selectinload(Interview.questions)
            .selectinload(InterviewQuestion.answer)
            .selectinload(InterviewAnswer.evaluation),
        ],
    )

    items: list[QuestionReportItem] = []
    overall_scores: list[float] = []
    communication_scores: list[float] = []
    technical_scores: list[float] = []
    word_counts: list[int] = []
    filler_counts: list[int] = []
    filler_ratios: list[float] = []
    difficulties: list[str] = []
    all_strengths: list[str] = []
    all_weaknesses: list[str] = []
    answered_count = 0

    for q in interview.questions:
        difficulties.append(q.difficulty)
        answer = q.answer
        evaluation = answer.evaluation if answer else None

        item = QuestionReportItem(
            question=QuestionResponse.model_validate(q),
            answer_content=answer.content if answer else None,
            answer_word_count=answer.word_count if answer else None,
            evaluation=EvaluationResponse.model_validate(evaluation) if evaluation else None,
        )
        items.append(item)

        if answer:
            answered_count += 1
            word_counts.append(answer.word_count)

        if evaluation:
            if evaluation.overall_score is not None:
                overall_scores.append(evaluation.overall_score)
            if evaluation.communication_score is not None:
                communication_scores.append(evaluation.communication_score)
            if evaluation.technical_accuracy_score is not None:
                technical_scores.append(evaluation.technical_accuracy_score)

            tf = evaluation.text_features or {}
            filler_counts.append(tf.get("filler_total", 0))
            filler_ratios.append(tf.get("filler_ratio", 0.0))

            all_strengths.extend(evaluation.strengths or [])
            all_weaknesses.extend(evaluation.weaknesses or [])

    summary = ReportSummary(
        questions_asked=len(interview.questions),
        questions_answered=answered_count,
        average_overall_score=_safe_mean(overall_scores),
        average_communication_score=_safe_mean(communication_scores),
        average_technical_accuracy_score=_safe_mean(technical_scores),
        average_word_count=_safe_mean(word_counts),
        total_filler_count=sum(filler_counts),
        average_filler_ratio=_safe_mean(filler_ratios),
        difficulty_progression=difficulties,
        # Deduplicate, keep order of first appearance, cap at 5
        strengths_summary=_unique_ordered(all_strengths)[:5],
        weaknesses_summary=_unique_ordered(all_weaknesses)[:5],
    )

    return InterviewReportResponse(
        interview=InterviewResponse.model_validate(interview),
        items=items,
        summary=summary,
    )


# ---------------------------------------------------------------------------
# Cross-interview analytics
# ---------------------------------------------------------------------------

def build_analytics_summary(db: Session, user: User) -> AnalyticsSummaryResponse:
    """Aggregate performance data across all of a user's interviews."""
    from sqlalchemy import select

    statement = (
        select(Interview)
        .where(Interview.user_id == user.id)
        .options(
            selectinload(Interview.questions)
            .selectinload(InterviewQuestion.answer)
            .selectinload(InterviewAnswer.evaluation),
        )
        .order_by(Interview.created_at)
    )
    interviews = list(db.scalars(statement).unique())

    total = len(interviews)
    completed = sum(1 for i in interviews if i.status == "completed")

    score_trend: list[float | None] = []
    all_overall: list[float] = []
    total_answered = 0
    topic_scores: dict[str, list[float]] = defaultdict(list)
    difficulty_dist: Counter[str] = Counter()
    type_dist: Counter[str] = Counter()
    history: list[InterviewHistoryItem] = []

    for interview in interviews:
        type_dist[interview.interview_type] += 1
        difficulty_dist[interview.starting_difficulty] += 1

        q_asked = len(interview.questions)
        q_answered = 0
        interview_scores: list[float] = []
        interview_word_counts: list[int] = []

        for q in interview.questions:
            answer = q.answer
            evaluation = answer.evaluation if answer else None

            if answer:
                q_answered += 1
                total_answered += 1
                interview_word_counts.append(answer.word_count)

            if evaluation and evaluation.overall_score is not None:
                interview_scores.append(evaluation.overall_score)
                all_overall.append(evaluation.overall_score)

                # Track by topic for strongest/weakest
                if q.topic:
                    topic_scores[q.topic].append(evaluation.overall_score)

        avg_score = _safe_mean(interview_scores)
        score_trend.append(avg_score)

        history.append(
            InterviewHistoryItem(
                interview_id=interview.id,
                role=interview.role,
                interview_type=interview.interview_type,
                difficulty=interview.starting_difficulty,
                status=interview.status,
                created_at=interview.created_at,
                questions_asked=q_asked,
                questions_answered=q_answered,
                average_overall_score=avg_score,
                average_word_count=_safe_mean(interview_word_counts),
            )
        )

    # Rank topics by average score
    ranked_topics = sorted(
        ((topic, _safe_mean(scores)) for topic, scores in topic_scores.items() if _safe_mean(scores) is not None),
        key=lambda t: t[1],  # type: ignore[arg-type]
        reverse=True,
    )
    strongest = [t[0] for t in ranked_topics[:5]]
    weakest = [t[0] for t in reversed(ranked_topics[-5:])] if len(ranked_topics) >= 2 else []

    # Rough time estimate: ~3 min per answered question
    time_estimate = total_answered * 3

    return AnalyticsSummaryResponse(
        total_interviews=total,
        completed_interviews=completed,
        total_questions_answered=total_answered,
        total_practice_time_estimate_minutes=time_estimate,
        average_overall_score=_safe_mean(all_overall),
        score_trend=score_trend,
        strongest_topics=strongest,
        weakest_topics=weakest,
        difficulty_distribution=dict(difficulty_dist),
        interview_type_distribution=dict(type_dist),
        history=history,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_mean(values: list[float | int]) -> float | None:
    """Return the arithmetic mean, or None if the list is empty."""
    return round(sum(values) / len(values), 2) if values else None


def _unique_ordered(items: list[str]) -> list[str]:
    """Deduplicate a list while preserving insertion order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
