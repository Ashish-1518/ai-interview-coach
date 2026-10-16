"""ML router for question difficulty classification."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.ml.difficulty_classifier import difficulty_classifier
from app.models.user import User
from app.schemas.difficulty_ml import DifficultyPredictRequest, DifficultyPredictResponse

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/predict-difficulty", response_model=DifficultyPredictResponse)
def predict_difficulty(
    payload: DifficultyPredictRequest,
    current_user: User = Depends(get_current_user),
) -> DifficultyPredictResponse:
    """Predict question difficulty using trained Scikit-Learn TF-IDF + Logistic Regression model."""
    result = difficulty_classifier.predict(payload.prompt)
    return DifficultyPredictResponse(
        prompt=payload.prompt,
        predicted_difficulty=str(result["predicted_difficulty"]),
        confidence=float(result["confidence"]),
        class_probabilities=dict(result["class_probabilities"]),  # type: ignore
        method=str(result["method"]),
    )
