from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

InterviewType = Literal["hr", "technical", "behavioral", "resume_based", "mixed"]
Difficulty = Literal["beginner", "intermediate", "advanced"]


class InterviewCreate(BaseModel):
    role: str = Field(min_length=2, max_length=120)
    interview_type: InterviewType = "mixed"
    difficulty: Difficulty = "intermediate"
    question_count: int = Field(default=5, ge=1, le=20)
    resume_id: str | None = None


class QuestionResponse(BaseModel):
    id: str
    position: int
    prompt: str
    topic: str
    difficulty: str
    question_type: str
    source: str
    concepts: list[str]

    model_config = {"from_attributes": True}


class InterviewResponse(BaseModel):
    id: str
    role: str
    interview_type: str
    starting_difficulty: str
    current_difficulty: str
    target_question_count: int
    status: str
    created_at: datetime
    completed_at: datetime | None
    questions: list[QuestionResponse] = []

    model_config = {"from_attributes": True}
