import re
from collections import Counter

from pydantic import BaseModel

FILLER_PHRASES = [
    "you know",
    "i mean",
    "kind of",
    "sort of",
    "basically",
    "actually",
    "literally",
    "honestly",
    "um",
    "uh",
    "like",
    "so",
]

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "that", "this", "these", "those",
    "is", "are", "was", "were", "be", "been", "being", "am", "do", "does", "did", "doing",
    "have", "has", "had", "having", "i", "you", "he", "she", "it", "we", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "its", "our", "their", "to", "of", "in", "on",
    "at", "for", "with", "about", "as", "by", "from", "into", "through", "during", "before",
    "after", "above", "below", "up", "down", "out", "off", "over", "under", "again", "further",
    "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "too",
    "very", "can", "will", "just", "should", "now", "also", "because", "while", "would", "could",
}

WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z'\-]*")
SENTENCE_SPLIT_PATTERN = re.compile(r"[.!?]+")


class TextFeatures(BaseModel):
    """Deterministic text measurements. These are counted, never predicted."""

    word_count: int
    sentence_count: int
    average_sentence_length: float
    filler_total: int
    filler_breakdown: dict[str, int]
    filler_ratio: float
    repeated_word_ratio: float
    repeated_phrases: list[str]


def extract_text_features(text: str) -> TextFeatures:
    """Compute countable language features from an answer.

    Every value here is produced by counting. No model, no LLM, no estimation.
    """

    lowered = text.lower()
    words = WORD_PATTERN.findall(lowered)
    word_count = len(words)

    sentences = [chunk.strip() for chunk in SENTENCE_SPLIT_PATTERN.split(text) if chunk.strip()]
    sentence_count = len(sentences) or (1 if text.strip() else 0)
    average_sentence_length = round(word_count / sentence_count, 2) if sentence_count else 0.0

    filler_breakdown: Counter[str] = Counter()
    for phrase in FILLER_PHRASES:
        occurrences = len(re.findall(rf"(?<![A-Za-z]){re.escape(phrase)}(?![A-Za-z])", lowered))
        if occurrences:
            filler_breakdown[phrase] = occurrences
    filler_total = sum(filler_breakdown.values())
    filler_ratio = round(filler_total / word_count, 4) if word_count else 0.0

    content_words = [word for word in words if word not in STOPWORDS]
    content_counter = Counter(content_words)
    repeated = {word: count for word, count in content_counter.items() if count > 1}
    repeated_word_ratio = (
        round(sum(count - 1 for count in repeated.values()) / len(content_words), 4) if content_words else 0.0
    )

    repeated_phrases = _find_repeated_bigrams(content_words)

    return TextFeatures(
        word_count=word_count,
        sentence_count=sentence_count,
        average_sentence_length=average_sentence_length,
        filler_total=filler_total,
        filler_breakdown=dict(filler_breakdown),
        filler_ratio=filler_ratio,
        repeated_word_ratio=repeated_word_ratio,
        repeated_phrases=repeated_phrases,
    )


def _find_repeated_bigrams(content_words: list[str], limit: int = 5) -> list[str]:
    bigrams = [f"{content_words[i]} {content_words[i + 1]}" for i in range(len(content_words) - 1)]
    counter = Counter(bigrams)
    return [phrase for phrase, count in counter.most_common(limit) if count > 1]
