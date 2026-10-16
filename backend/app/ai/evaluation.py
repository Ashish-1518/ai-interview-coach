from pydantic import BaseModel, Field


class LLMEvaluationResult(BaseModel):
    """Schema that the LLM must return when grading an answer.

    Validated with Pydantic before anything uses it. If the model returns
    something that does not match this shape, the evaluation is rejected.
    """

    overall_score: float = Field(ge=0, le=100)
    relevance: float = Field(ge=0, le=100)
    technical_accuracy: float = Field(ge=0, le=100)
    completeness: float = Field(ge=0, le=100)
    communication: float = Field(ge=0, le=100)
    structure: float = Field(ge=0, le=100)
    specificity: float = Field(ge=0, le=100)
    strengths: list[str] = Field(max_length=5)
    weaknesses: list[str] = Field(max_length=5)
    suggestions: list[str] = Field(max_length=5)


class STAREvaluationResult(BaseModel):
    """STAR breakdown for behavioral answers."""

    situation: float = Field(ge=0, le=25)
    task: float = Field(ge=0, le=25)
    action: float = Field(ge=0, le=25)
    result: float = Field(ge=0, le=25)
    feedback: str = Field(max_length=500)


EVALUATION_SYSTEM_PROMPT = """You are an expert interview evaluator.
You will receive an interview question and the candidate's answer.
Evaluate the answer and return JSON with exactly these keys:
  overall_score, relevance, technical_accuracy, completeness,
  communication, structure, specificity (each 0-100),
  strengths (list of up to 5 short strings),
  weaknesses (list of up to 5 short strings),
  suggestions (list of up to 5 short strings).

Be fair and honest. Do not inflate scores.
A vague or off-topic answer should score below 50.
A correct but shallow answer should score 50-70.
A thorough, structured, specific answer should score 70-90.
A near-perfect answer should score 90-100.
Do not generate meaningless or randomly correlated scores."""


STAR_EVALUATION_SYSTEM_PROMPT = """You are an expert interview evaluator.
The candidate was asked a behavioral question. Evaluate their answer using the STAR framework.
Return JSON with exactly these keys:
  situation (0-25), task (0-25), action (0-25), result (0-25),
  feedback (a short paragraph explaining how to improve).
If the candidate did not mention a component, score it 0 and say so in feedback."""


def build_evaluation_prompt(question_prompt: str, answer_content: str) -> str:
    return (
        f"Interview Question:\n{question_prompt}\n\n"
        f"Candidate's Answer:\n{answer_content}"
    )
