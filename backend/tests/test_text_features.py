from app.nlp.text_features import extract_text_features


def test_counts_words_and_sentences() -> None:
    text = "Machine learning uses data to train models. It is widely used in industry."
    features = extract_text_features(text)

    assert features.word_count == 13
    assert features.sentence_count == 2
    assert features.average_sentence_length == 6.5


def test_detects_filler_words() -> None:
    text = "So basically I like used Python and um basically built a model you know."
    features = extract_text_features(text)

    assert features.filler_total >= 4
    assert "basically" in features.filler_breakdown
    assert "um" in features.filler_breakdown
    assert features.filler_ratio > 0


def test_detects_repeated_words() -> None:
    text = "Python Python Python is is great great for data data science."
    features = extract_text_features(text)

    assert features.repeated_word_ratio > 0


def test_empty_text_returns_zero_features() -> None:
    features = extract_text_features("")

    assert features.word_count == 0
    assert features.filler_total == 0
    assert features.filler_ratio == 0.0
