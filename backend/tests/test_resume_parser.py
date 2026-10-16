from app.services.resume_parser import parse_resume_text


def test_parse_resume_text_extracts_grounded_information() -> None:
    raw_text = """
    Asha Student
    asha@example.com
    +91 9876543210

    Skills
    Python, SQL, Machine Learning, FastAPI

    Education
    B.Tech Computer Science and Engineering AIML

    Projects
    AI Interview Coach using Python and FastAPI
    """

    parsed = parse_resume_text(raw_text)

    assert parsed.name == "Asha Student"
    assert parsed.emails == ["asha@example.com"]
    assert "Python" in parsed.skills
    assert "Fastapi" in parsed.skills
    assert parsed.education == ["B.Tech Computer Science and Engineering AIML"]
    assert parsed.projects == ["AI Interview Coach using Python and FastAPI"]
