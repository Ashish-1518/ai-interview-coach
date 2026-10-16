from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.question_bank import QuestionBankItem

SUPPORTED_ROLES = [
    "Software Developer",
    "Full Stack Developer",
    "Python Developer",
    "Java Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Backend Developer",
    "Frontend Developer",
]

# Curated questions written by hand. Minimal but real: the engine has genuine
# content to serve with no AI provider configured. More entries are added by editing
# this list or via the seed command.
SEED_QUESTIONS: list[dict] = [
    {
        "role": "Machine Learning Engineer",
        "interview_type": "technical",
        "difficulty": "beginner",
        "topic": "Machine Learning Fundamentals",
        "prompt": "What is the difference between supervised and unsupervised learning?",
        "concepts": ["labeled data", "clustering", "classification vs regression"],
    },
    {
        "role": "Machine Learning Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "topic": "Model Evaluation",
        "prompt": "Explain the bias-variance tradeoff and how it affects model performance.",
        "concepts": ["underfitting", "overfitting", "generalization", "regularization"],
    },
    {
        "role": "Machine Learning Engineer",
        "interview_type": "technical",
        "difficulty": "advanced",
        "topic": "Model Evaluation",
        "prompt": "How would you detect and handle data leakage in a production ML pipeline?",
        "concepts": ["train/test contamination", "temporal splits", "feature leakage"],
    },
    {
        "role": "Python Developer",
        "interview_type": "technical",
        "difficulty": "beginner",
        "topic": "Python Basics",
        "prompt": "What is the difference between a list and a tuple in Python?",
        "concepts": ["mutability", "performance", "hashability"],
    },
    {
        "role": "Python Developer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "topic": "Python Internals",
        "prompt": "How does Python's garbage collection work?",
        "concepts": ["reference counting", "cyclic garbage collector", "memory management"],
    },
    {
        "role": "Backend Developer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "topic": "Databases",
        "prompt": "Explain database indexing and when an index can hurt performance.",
        "concepts": ["B-tree", "query planner", "write overhead", "selectivity"],
    },
    {
        "role": "Backend Developer",
        "interview_type": "technical",
        "difficulty": "advanced",
        "topic": "System Design",
        "prompt": "How would you design an API to handle a sudden tenfold traffic spike?",
        "concepts": ["horizontal scaling", "caching", "rate limiting", "load balancing"],
    },
    {
        "role": "Backend Developer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "topic": "APIs",
        "prompt": "How do you handle authentication and authorization in a REST API?",
        "concepts": ["JWT", "roles and scopes", "middleware", "token expiry"],
    },
    {
        "role": "Software Developer",
        "interview_type": "hr",
        "difficulty": "beginner",
        "topic": "Introduction",
        "prompt": "Tell me about yourself.",
        "concepts": ["background", "skills", "motivation"],
    },
    {
        "role": "Software Developer",
        "interview_type": "behavioral",
        "difficulty": "intermediate",
        "topic": "Teamwork",
        "prompt": "Describe a time you disagreed with a teammate. How did you handle it?",
        "concepts": ["situation", "task", "action", "result"],
    },
    {
        "role": "Data Scientist",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "topic": "Statistics",
        "prompt": "How would you handle missing values in a dataset before training a model?",
        "concepts": ["imputation", "missingness mechanism", "dropping rows vs columns"],
    },
]


def seed_question_bank(db: Session) -> int:
    """Insert curated questions that are not already present. Returns rows added."""

    inserted = 0
    for entry in SEED_QUESTIONS:
        exists = db.scalar(
            select(QuestionBankItem).where(
                QuestionBankItem.role == entry["role"],
                QuestionBankItem.prompt == entry["prompt"],
            )
        )
        if exists is None:
            db.add(QuestionBankItem(**entry))
            inserted += 1
    db.commit()
    return inserted
