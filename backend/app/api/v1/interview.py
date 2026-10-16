from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.dependencies import get_llm_provider
from app.ai.schemas import LLMProvider
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.answer import AnswerSubmit
from app.schemas.evaluation import AnswerWithEvaluationResponse, EvaluationResponse
from app.schemas.interview import InterviewCreate, InterviewResponse, QuestionResponse
from app.services.evaluation_service import AnswerAlreadyExistsError, submit_and_evaluate
from app.services.interview_service import (
    InterviewNotFoundError,
    InterviewStateError,
    ask_next_question,
    complete_interview,
    create_interview,
    get_interview_for_user,
    list_interviews_for_user,
)
from app.services.question_service import NoQuestionAvailableError

router = APIRouter(prefix="/interviews", tags=["interviews"])


def _load_interview(db: Session, user: User, interview_id: str):
    interview = get_interview_for_user(db, user, interview_id)
    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
    return interview


@router.post("", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def start_interview(
    interview_in: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InterviewResponse:
    interview = create_interview(db, current_user, interview_in)
    return InterviewResponse.model_validate(interview)


@router.get("", response_model=list[InterviewResponse])
def list_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[InterviewResponse]:
    return [InterviewResponse.model_validate(item) for item in list_interviews_for_user(db, current_user)]


@router.get("/{interview_id}", response_model=InterviewResponse)
def read_interview(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InterviewResponse:
    return InterviewResponse.model_validate(_load_interview(db, current_user, interview_id))


@router.post("/{interview_id}/next", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def next_question(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    provider: LLMProvider | None = Depends(get_llm_provider),
) -> QuestionResponse:
    interview = _load_interview(db, current_user, interview_id)
    try:
        question = ask_next_question(db, interview, provider)
    except NoQuestionAvailableError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except InterviewStateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return QuestionResponse.model_validate(question)


@router.post("/{interview_id}/complete", response_model=InterviewResponse)
def finish_interview(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InterviewResponse:
    interview = _load_interview(db, current_user, interview_id)
    interview = complete_interview(db, interview)
    return InterviewResponse.model_validate(interview)


@router.post(
    "/{interview_id}/questions/{question_id}/answers",
    response_model=AnswerWithEvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_answer(
    interview_id: str,
    question_id: str,
    answer_in: AnswerSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    provider: LLMProvider | None = Depends(get_llm_provider),
) -> AnswerWithEvaluationResponse:
    interview = _load_interview(db, current_user, interview_id)
    question = next((q for q in interview.questions if q.id == question_id), None)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found in this interview.")
    try:
        answer, evaluation = submit_and_evaluate(db, question, answer_in, provider)
    except AnswerAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return AnswerWithEvaluationResponse(
        answer_id=answer.id,
        question_id=question.id,
        word_count=answer.word_count,
        evaluation=EvaluationResponse.model_validate(evaluation),
    )
