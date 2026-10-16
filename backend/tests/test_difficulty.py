import pytest

from app.services.difficulty import next_difficulty


def test_strong_performance_raises_difficulty_one_level() -> None:
    assert next_difficulty("beginner", [85, 90]) == "intermediate"
    assert next_difficulty("intermediate", [85, 90]) == "advanced"


def test_weak_performance_lowers_difficulty_one_level() -> None:
    assert next_difficulty("advanced", [30, 40]) == "intermediate"
    assert next_difficulty("intermediate", [30, 40]) == "beginner"


def test_middle_performance_keeps_difficulty() -> None:
    assert next_difficulty("intermediate", [70, 65]) == "intermediate"


def test_difficulty_never_goes_below_beginner_or_above_advanced() -> None:
    assert next_difficulty("beginner", [10, 20]) == "beginner"
    assert next_difficulty("advanced", [95, 99]) == "advanced"


def test_no_scores_keeps_difficulty() -> None:
    assert next_difficulty("intermediate", []) == "intermediate"


def test_unknown_difficulty_raises() -> None:
    with pytest.raises(ValueError):
        next_difficulty("expert", [90, 90])
