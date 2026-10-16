import math
import re
from collections import Counter

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
RELATED_SKILL_GROUPS = [
    {"javascript", "typescript", "nodejs", "react", "frontend", "web"},
    {"python", "pandas", "numpy", "scikitlearn", "pytorch", "tensorflow", "ml", "machinelearning"},
    {"sql", "postgresql", "mysql", "database", "indexing", "query"},
    {"docker", "kubernetes", "container", "deployment", "devops", "ci", "cd"},
    {"api", "rest", "http", "endpoint", "fastapi", "backend", "server"},
]


class TfidfVectorizer:
    """Minimal pure-Python TF-IDF vectorizer with cosine similarity.

    Implemented using Python's standard library (math, Counter) so it runs with zero
    external dependencies while keeping the exact TF-IDF mathematical formulation:
      IDF(t) = ln((1 + N) / (1 + DF(t))) + 1
      Cosine Sim(u, v) = (u · v) / (||u|| * ||v||)
    """

    def __init__(self) -> None:
        self._vocabulary: dict[str, int] = {}
        self._idf: list[float] = []

    def fit(self, documents: list[str]) -> "TfidfVectorizer":
        document_tokens = [self._tokenize(document) for document in documents]
        document_count = len(document_tokens) or 1

        vocabulary: set[str] = set()
        for tokens in document_tokens:
            vocabulary.update(tokens)

        sorted_vocab = sorted(vocabulary)
        self._vocabulary = {term: index for index, term in enumerate(sorted_vocab)}

        document_frequency = [0.0] * len(self._vocabulary)
        for tokens in document_tokens:
            for term in set(tokens):
                document_frequency[self._vocabulary[term]] += 1.0

        self._idf = [
            math.log((1.0 + document_count) / (1.0 + df)) + 1.0
            for df in document_frequency
        ]
        return self

    def transform(self, document: str) -> list[float]:
        if not self._idf:
            raise RuntimeError("TfidfVectorizer must be fitted before calling transform.")

        vector = [0.0] * len(self._vocabulary)
        tokens = self._tokenize(document)
        if not tokens:
            return vector

        counts = Counter(tokens)
        for term, count in counts.items():
            index = self._vocabulary.get(term)
            if index is not None:
                vector[index] = count * self._idf[index]

        norm = math.sqrt(sum(x * x for x in vector))
        return [x / norm for x in vector] if norm > 0 else vector

    @staticmethod
    def cosine_similarity(first: list[float], second: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(first, second))
        norm_a = math.sqrt(sum(a * a for a in first))
        norm_b = math.sqrt(sum(b * b for b in second))
        denominator = norm_a * norm_b
        if denominator == 0:
            return 0.0
        return float(dot_product / denominator)

    def similarity(self, first: str, second: str) -> float:
        return self.cosine_similarity(self.transform(first), self.transform(second))

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())


def related_terms(word: str) -> set[str]:
    for group in RELATED_SKILL_GROUPS:
        if word in group:
            return group
    return {word}


def relaxed_concept_coverage(answer: str, concepts: list[str]) -> float:
    """Measure how much of a question's expected concepts an answer covers.

    A concept counts as covered when its words appear in the answer, or when a
    closely related term appears (for example "js" for "javascript").
    This is transparent lexical matching, not semantic understanding.
    """

    if not concepts:
        return 0.0

    answer_tokens = set(TOKEN_PATTERN.findall(answer.lower()))
    covered = 0
    for concept in concepts:
        concept_tokens = [token for token in TOKEN_PATTERN.findall(concept.lower()) if len(token) > 2]
        if not concept_tokens:
            continue
        matched = 0
        for token in concept_tokens:
            if token in answer_tokens or answer_tokens & related_terms(token):
                matched += 1
        if matched / len(concept_tokens) >= 0.5:
            covered += 1

    return round(covered / len(concepts), 4)


def deterministic_relevance(answer: str, question_prompt: str, concepts: list[str]) -> float:
    """Combine lexical overlap with expected-concept coverage into a 0-100 signal."""

    vectorizer = TfidfVectorizer().fit([question_prompt, answer])
    overlap = vectorizer.similarity(question_prompt, answer)
    coverage = relaxed_concept_coverage(answer, concepts)

    # Weighted blend: concept coverage matters more than raw word overlap.
    score = (0.4 * overlap + 0.6 * coverage) * 100
    return round(min(100.0, max(0.0, score)), 2)
