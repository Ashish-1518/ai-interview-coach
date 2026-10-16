from collections.abc import Sequence

DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]

# Documented heuristic thresholds. These are rules, not predictions.
STRONG_MEAN_THRESHOLD = 80
WEAK_MEAN_THRESHOLD = 50
RECENT_WINDOW = 2


def next_difficulty(current: str, recent_overall_scores: Sequence[float]) -> str:
    """Adjust difficulty by a documented rule based on the last two scores.

    - Mean of the recent scores >= 80 raises difficulty one level.
    - Mean of the recent scores < 50 lowers difficulty one level.
    - Otherwise difficulty stays the same.
    - Never skips a level, and never moves past beginner or advanced.
    """

    if current not in DIFFICULTY_LEVELS:
        raise ValueError(f"Unknown difficulty level: {current}")

    if not recent_overall_scores:
        return current

    window = list(recent_overall_scores)[-RECENT_WINDOW:]
    mean_score = sum(window) / len(window)
    index = DIFFICULTY_LEVELS.index(current)

    if mean_score >= STRONG_MEAN_THRESHOLD and index < len(DIFFICULTY_LEVELS) - 1:
        return DIFFICULTY_LEVELS[index + 1]
    if mean_score < WEAK_MEAN_THRESHOLD and index > 0:
        return DIFFICULTY_LEVELS[index - 1]
    return current
