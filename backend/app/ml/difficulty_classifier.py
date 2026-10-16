"""Scikit-learn / pure-Python based question difficulty classifier.

KEY DESIGN CHOICES (for your viva):

1. Dual-Engine Architecture:
   - Uses `scikit-learn`'s `TfidfVectorizer` + `LogisticRegression` pipeline when installed.
   - Falls back seamlessly to our pure-Python `TfidfVectorizer` + Cosine Nearest Neighbor
     classifier when `scikit-learn` is absent, guaranteeing zero binary dependencies.

2. Explainable Probability Calibration:
   Returns predicted class along with probability confidence breakdown across
   'beginner', 'intermediate', and 'advanced'.
"""
import math
from typing import Any, Literal

DifficultyLevel = Literal["beginner", "intermediate", "advanced"]

# Training dataset curated from domain question bank patterns
TRAINING_DATA = [
    # Beginner
    ("What is a list in Python?", "beginner"),
    ("How do you declare a variable in JavaScript?", "beginner"),
    ("What is the difference between a tuple and a list?", "beginner"),
    ("Explain the basic SELECT statement in SQL.", "beginner"),
    ("What is an HTML tag?", "beginner"),
    ("How do you write a comment in Python?", "beginner"),
    ("What does CSS stand for?", "beginner"),
    ("What is a function in programming?", "beginner"),
    # Intermediate
    ("How do REST APIs handle authentication using JSON Web Tokens?", "intermediate"),
    ("Explain indexing in PostgreSQL and how it improves query performance.", "intermediate"),
    ("What is the difference between synchronous and asynchronous execution in Node.js?", "intermediate"),
    ("How does React's virtual DOM reconciliation work under the hood?", "intermediate"),
    ("Explain object-oriented programming principles like encapsulation and inheritance.", "intermediate"),
    ("How do you handle database migrations using Alembic?", "intermediate"),
    ("What is Docker containerization and how does it differ from virtual machines?", "intermediate"),
    # Advanced
    ("Design a distributed rate limiter that handles 100k requests per second across regions.", "advanced"),
    ("Explain the internal mechanics of B-tree vs LSM-tree storage engines in high-throughput databases.", "advanced"),
    ("How would you architect a fault-tolerant microservices system with event-driven saga pattern?", "advanced"),
    ("Discuss memory management, garbage collection overhead, and GIL workarounds in multi-threaded CPython.", "advanced"),
    ("How do Transformer attention mechanisms optimize parallel computation compared to recurrent neural networks?", "advanced"),
    ("Design a global high-availability distributed cache with vector search capability.", "advanced"),
]


try:
    from sklearn.feature_extraction.text import TfidfVectorizer as SklearnTfidf
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    from app.ml.similarity import TfidfVectorizer as PureTfidf


class QuestionDifficultyClassifier:
    """Classifier for question difficulty using Scikit-Learn or Pure-Python TF-IDF."""

    def __init__(self) -> None:
        self.model: Any = None
        self.has_sklearn = HAS_SKLEARN
        self.fit_model()

    def fit_model(self) -> None:
        """Fit classifier on training data."""
        texts, labels = zip(*TRAINING_DATA)

        if HAS_SKLEARN:
            self.model = Pipeline(
                [
                    ("tfidf", SklearnTfidf(ngram_range=(1, 2), min_df=1)),
                    ("clf", LogisticRegression(random_state=42, C=1.0)),
                ]
            )
            self.model.fit(texts, labels)
        else:
            # Pure Python TF-IDF Nearest Neighbor Classifier
            self.pure_tfidf = PureTfidf().fit(list(texts))
            self.train_vectors = [self.pure_tfidf.transform(t) for t in texts]
            self.train_labels = list(labels)

    def predict(self, prompt: str) -> dict[str, str | float | dict[str, float]]:
        """Predict difficulty class and confidence probabilities for a prompt."""
        if not prompt.strip():
            return self._fallback_prediction(prompt)

        if self.has_sklearn and self.model is not None:
            try:
                predicted_class = str(self.model.predict([prompt])[0])
                probabilities = self.model.predict_proba([prompt])[0]
                class_probs = {
                    cls: round(float(prob), 4)
                    for cls, prob in zip(self.model.classes_, probabilities)
                }
                confidence = round(float(max(probabilities)), 4)

                return {
                    "predicted_difficulty": predicted_class,
                    "confidence": confidence,
                    "class_probabilities": class_probs,
                    "method": "ml:sklearn_tfidf_logistic_regression",
                }
            except Exception:
                return self._fallback_prediction(prompt)

        # Pure-Python TF-IDF Cosine Similarity K-NN Classifier
        try:
            vec = self.pure_tfidf.transform(prompt)
            sims = [
                (self.pure_tfidf.cosine_similarity(vec, train_vec), label)
                for train_vec, label in zip(self.train_vectors, self.train_labels)
            ]
            sims.sort(key=lambda x: x[0], reverse=True)

            # Softmax style probability over top similarities per class
            class_scores: dict[str, float] = {"beginner": 0.1, "intermediate": 0.1, "advanced": 0.1}
            for sim, label in sims[:6]:
                class_scores[label] += max(0.0, sim)

            total = sum(class_scores.values())
            class_probs = {cls: round(score / total, 4) for cls, score in class_scores.items()}
            predicted_class = max(class_probs.items(), key=lambda x: x[1])[0]
            confidence = class_probs[predicted_class]

            return {
                "predicted_difficulty": predicted_class,
                "confidence": confidence,
                "class_probabilities": class_probs,
                "method": "ml:pure_python_tfidf_knn",
            }
        except Exception:
            return self._fallback_prediction(prompt)

    def _fallback_prediction(self, prompt: str) -> dict[str, str | float | dict[str, float]]:
        """Deterministic heuristic fallback if model fails."""
        words = prompt.split()
        word_count = len(words)

        if word_count < 10:
            diff = "beginner"
        elif word_count < 22:
            diff = "intermediate"
        else:
            diff = "advanced"

        return {
            "predicted_difficulty": diff,
            "confidence": 0.50,
            "class_probabilities": {"beginner": 0.33, "intermediate": 0.33, "advanced": 0.34},
            "method": "heuristic:word_count_fallback",
        }


# Global singleton instance
difficulty_classifier = QuestionDifficultyClassifier()
