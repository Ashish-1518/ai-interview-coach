from typing import Any

from pydantic import BaseModel


class EvaluationResponse(BaseModel):
    id: str
    answer_id: str
    overall_score: float | None
    relevance_score: float | None
    technical_accuracy_score: float | None
    completeness_score: float | None
    communication_score: float | None
    structure_score: float | None
    specificity_score: float | None
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    star_evaluation: dict[str, Any] | None
    text_features: dict[str, Any]
    method_map: dict[str, str]

    model_config = {"from_attributes": True}


class AnswerWithEvaluationResponse(BaseModel):
    answer_id: str
    question_id: str
    word_count: int
    evaluation: EvaluationResponse
