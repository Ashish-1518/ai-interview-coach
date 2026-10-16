"""Voice and speech analytics service.

KEY DESIGN CHOICES (for your viva):

1. Speaking Pace (WPM):
   WPM = (Word Count / Audio Duration in Seconds) * 60

   Benchmark bounds (ideal interview speech):
   - < 110 WPM: Too slow (hesitant)
   - 110 - 160 WPM: Optimal conversational speed
   - > 160 WPM: Too fast (rushed)

2. Pause Estimation:
   Calculated deterministically using punctuation frequency (periods, commas, dashes)
   and expected word duration vs actual audio duration.

3. Clarity Score (0-100):
   Starts at 100, penalizing for filler word ratio and extreme WPM deviations.
   All formulas are deterministic counting, with method provenance recorded.
"""
from app.nlp.text_features import extract_text_features
from app.schemas.voice import VoiceAnalysisRequest, VoiceAnalysisResponse


def analyze_voice_transcript(payload: VoiceAnalysisRequest) -> VoiceAnalysisResponse:
    """Analyze a transcript alongside audio duration to produce speech metrics."""

    tf = extract_text_features(payload.transcript)
    duration_min = payload.duration_seconds / 60.0

    # 1. Speaking Pace (WPM)
    wpm = round(tf.word_count / duration_min, 1) if duration_min > 0 else 0.0

    if wpm < 110:
        pace_status = "too_slow"
    elif wpm <= 160:
        pace_status = "optimal"
    else:
        pace_status = "too_fast"

    # 2. Pause estimation based on punctuation count and duration excess
    punctuation_pauses = payload.transcript.count(".") + payload.transcript.count(",") + payload.transcript.count(";")
    # Expected speaking time at ideal 135 WPM
    expected_sec = (tf.word_count / 135.0) * 60.0
    excess_sec = max(0.0, payload.duration_seconds - expected_sec)
    duration_pauses = int(excess_sec / 2.5)  # Assume ~2.5s per extra long pause

    estimated_pauses = max(punctuation_pauses, duration_pauses)

    # 3. Clarity Score calculation (100 base, deducted for fillers and bad pace)
    clarity = 100.0

    # Filler deduction (up to -30 points)
    filler_penalty = min(30.0, tf.filler_ratio * 200.0)
    clarity -= filler_penalty

    # Pace deduction (up to -20 points if outside 110-160 optimal zone)
    if wpm < 110:
        pace_penalty = min(20.0, (110 - wpm) * 0.4)
        clarity -= pace_penalty
    elif wpm > 160:
        pace_penalty = min(20.0, (wpm - 160) * 0.4)
        clarity -= pace_penalty

    clarity_score = round(max(0.0, min(100.0, clarity)), 1)

    return VoiceAnalysisResponse(
        speaking_pace_wpm=wpm,
        pace_status=pace_status,
        estimated_pauses=estimated_pauses,
        clarity_score=clarity_score,
        text_features=tf,
        method_map={
            "speaking_pace": "deterministic:wpm_ratio",
            "estimated_pauses": "heuristic:punctuation_duration_delta",
            "clarity_score": "rule_based:filler_pace_deductions",
        },
    )
