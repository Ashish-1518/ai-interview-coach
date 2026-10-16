QUESTION_SYSTEM_PROMPT = """You are a professional interviewer conducting a mock interview.
Ask exactly one interview question.
Base the question on the target role, interview type, and requested difficulty.
Do not include the answer. Do not include multiple questions.
Return JSON with the keys: prompt, topic, difficulty, concepts.
difficulty must be one of: beginner, intermediate, advanced.
concepts must be a short list of ideas a strong answer would cover.
Never invent facts about the candidate's resume."""


def build_question_prompt(
    role: str,
    interview_type: str,
    difficulty: str,
    avoid_prompts: list[str],
) -> str:
    avoid_block = "\n".join(f"- {prompt}" for prompt in avoid_prompts) or "- none"
    return (
        f"Target role: {role}\n"
        f"Interview type: {interview_type}\n"
        f"Requested difficulty: {difficulty}\n\n"
        "Do not repeat or paraphrase any of these previously asked questions:\n"
        f"{avoid_block}"
    )
