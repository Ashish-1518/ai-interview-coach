import re
from collections.abc import Iterable
from pathlib import Path

from pypdf import PdfReader

from app.schemas.resume import ParsedResumeData

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){10,12}")

KNOWN_SKILLS = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "computer vision",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "docker",
    "git",
    "linux",
    "aws",
    "azure",
    "html",
    "css",
}

SECTION_HEADERS = {
    "education": ["education", "academic background"],
    "projects": ["projects", "project experience"],
    "experience": ["experience", "work experience", "internship", "internships"],
    "certifications": ["certifications", "certificates"],
    "achievements": ["achievements", "awards"],
}


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file without applying AI interpretation."""

    reader = PdfReader(str(file_path))
    page_texts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            page_texts.append(text)
    return "\n".join(page_texts).strip()


def parse_resume_text(raw_text: str) -> ParsedResumeData:
    """Parse resume text using transparent heuristics, not fake AI."""

    normalized_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return ParsedResumeData(
        name=_guess_name(normalized_lines),
        emails=sorted(set(EMAIL_PATTERN.findall(raw_text))),
        phone_numbers=_extract_phone_numbers(raw_text),
        skills=_extract_skills(raw_text),
        education=_extract_section_lines(normalized_lines, "education"),
        projects=_extract_section_lines(normalized_lines, "projects"),
        experience=_extract_section_lines(normalized_lines, "experience"),
        certifications=_extract_section_lines(normalized_lines, "certifications"),
        achievements=_extract_section_lines(normalized_lines, "achievements"),
    )


def _guess_name(lines: list[str]) -> str | None:
    for line in lines[:5]:
        lower = line.lower()
        if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line):
            continue
        if any(marker in lower for marker in ("resume", "curriculum vitae", "linkedin", "github")):
            continue
        if 1 <= len(line.split()) <= 4:
            return line
    return None


def _extract_phone_numbers(text: str) -> list[str]:
    candidates = PHONE_PATTERN.findall(text)
    cleaned = {re.sub(r"\s+", " ", candidate).strip() for candidate in candidates}
    return sorted(number for number in cleaned if len(re.sub(r"\D", "", number)) >= 10)


def _extract_skills(text: str) -> list[str]:
    lower_text = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        if re.search(rf"(?<![A-Za-z0-9+#.]){re.escape(skill)}(?![A-Za-z0-9+#.])", lower_text):
            found.append(_format_skill(skill))
    return sorted(found)


def _format_skill(skill: str) -> str:
    special = {
        "c++": "C++",
        "node.js": "Node.js",
        "nlp": "NLP",
        "sql": "SQL",
        "aws": "AWS",
        "html": "HTML",
        "css": "CSS",
    }
    return special.get(skill, skill.title())


def _extract_section_lines(lines: list[str], section: str) -> list[str]:
    start_index = _find_section_start(lines, SECTION_HEADERS[section])
    if start_index is None:
        return []

    collected: list[str] = []
    for line in lines[start_index + 1 :]:
        if _looks_like_any_section_header(line, SECTION_HEADERS.values()):
            break
        collected.append(line)
        if len(collected) >= 8:
            break
    return collected


def _find_section_start(lines: list[str], aliases: list[str]) -> int | None:
    aliases_lower = {alias.lower() for alias in aliases}
    for index, line in enumerate(lines):
        cleaned = line.strip().lower().rstrip(":")
        if cleaned in aliases_lower:
            return index
    return None


def _looks_like_any_section_header(line: str, alias_groups: Iterable[list[str]]) -> bool:
    cleaned = line.strip().lower().rstrip(":")
    return any(cleaned in {alias.lower() for alias in aliases} for aliases in alias_groups)
