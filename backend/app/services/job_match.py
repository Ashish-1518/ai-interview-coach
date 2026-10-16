"""Job matching and skill-gap analysis service.

KEY DESIGN CHOICES (for your viva):

1. Skill extraction uses transparent keyword matching against standard skill lists
   rather than opaque black-box models. Every skill found can be pointed to in text.

2. Semantic similarity uses TF-IDF vectorization and Cosine Similarity
   (from app.ml.similarity), providing an explainable mathematical metric for text overlap.

3. The overall fit score blends discrete skill coverage (60%) with semantic text
   relevance (40%). The method_map explicitly records provenance for every component.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ml.similarity import TfidfVectorizer
from app.models.resume import Resume
from app.models.user import User
from app.schemas.job_match import JobMatchRequest, JobMatchResponse, SkillGapAnalysis
from app.services.resume_parser import KNOWN_SKILLS, _extract_skills


class ResumeNotFoundError(Exception):
    """Raised when no suitable resume is found for the user."""


def perform_job_match(db: Session, user: User, payload: JobMatchRequest) -> JobMatchResponse:
    """Analyze fit between a user's resume and a target job description."""

    # 1. Resolve resume (specific ID or user's latest)
    if payload.resume_id:
        statement = select(Resume).where(Resume.id == payload.resume_id, Resume.user_id == user.id)
        resume = db.scalar(statement)
    else:
        statement = select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc()).limit(1)
        resume = db.scalar(statement)

    if not resume:
        raise ResumeNotFoundError("No resume found. Upload a resume before running job matching.")

    # 2. Extract skills from Job Description text
    jd_skills = _extract_skills(payload.jd_text)

    # 3. Get resume skills (from parsed data or fallback re-extraction)
    parsed_skills = []
    if isinstance(resume.parsed_data, dict):
        parsed_skills = resume.parsed_data.get("skills", [])
    if not parsed_skills and resume.raw_text:
        parsed_skills = _extract_skills(resume.raw_text)

    # Normalize comparison (case-insensitive sets)
    resume_skill_set = {s.lower() for s in parsed_skills}
    jd_skill_set = {s.lower() for s in jd_skills}

    # 4. Skill gap calculations
    matched_set = resume_skill_set & jd_skill_set
    missing_set = jd_skill_set - resume_skill_set
    bonus_set = resume_skill_set - jd_skill_set

    # Map back to formatted names
    matched_skills = sorted([s for s in parsed_skills if s.lower() in matched_set])
    missing_skills = sorted([_format_skill_name(s) for s in missing_set])
    bonus_skills = sorted([s for s in parsed_skills if s.lower() in bonus_set])

    # Skill match score (0-100%)
    if jd_skill_set:
        skill_score = round((len(matched_set) / len(jd_skill_set)) * 100, 2)
    else:
        skill_score = 100.0 if not jd_skill_set and resume_skill_set else 50.0

    # 5. Semantic similarity calculation (TF-IDF + Cosine Similarity)
    tfidf = TfidfVectorizer()
    resume_text = resume.raw_text or ""
    tfidf.fit([resume_text, payload.jd_text])
    raw_similarity = tfidf.similarity(resume_text, payload.jd_text)
    # Cosine similarity for document vectors usually ranges 0.0 - 1.0; scale to 0-100
    semantic_score = round(raw_similarity * 100, 2)

    # 6. Weighted overall fit score
    overall_score = round((0.6 * skill_score) + (0.4 * semantic_score), 2)
    overall_score = min(100.0, max(0.0, overall_score))

    # 7. Preparation recommendations based on gaps
    recommendations = _generate_recommendations(missing_skills, skill_score, overall_score)

    return JobMatchResponse(
        resume_id=resume.id,
        role_title=payload.role_title,
        extracted_jd_skills=jd_skills,
        extracted_resume_skills=parsed_skills,
        skill_gap=SkillGapAnalysis(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            bonus_skills=bonus_skills,
            skill_match_percentage=skill_score,
        ),
        semantic_similarity_score=semantic_score,
        overall_fit_score=overall_score,
        recommendations=recommendations,
        method_map={
            "skill_match": "heuristic:set_intersection",
            "semantic_similarity": "ml:tfidf_cosine",
            "overall_fit": "weighted_blend:60_skill_40_semantic",
        },
    )


def _format_skill_name(skill_lower: str) -> str:
    """Format lowercase skill slug to canonical display name."""
    special = {
        "c++": "C++",
        "node.js": "Node.js",
        "nlp": "NLP",
        "sql": "SQL",
        "aws": "AWS",
        "html": "HTML",
        "css": "CSS",
    }
    return special.get(skill_lower, skill_lower.title())


def _generate_recommendations(missing_skills: list[str], skill_score: float, overall_score: float) -> list[str]:
    """Build practical preparation recommendations for the candidate."""
    recs: list[str] = []

    if missing_skills:
        top_missing = missing_skills[:4]
        recs.append(f"Focus technical prep on key missing skills: {', '.join(top_missing)}.")
        recs.append("Add relevant projects or coursework demonstrating experience with these topics to your resume.")

    if skill_score < 50.0:
        recs.append("Consider starting with Beginner difficulty technical interviews to build core topic familiarity.")
    elif skill_score >= 80.0:
        recs.append("Strong skill match! Practice Advanced difficulty mock interviews focused on architecture and trade-offs.")
    else:
        recs.append("Moderate skill match. Practice Intermediate level technical mock interviews.")

    if overall_score < 60.0:
        recs.append("Tailor your resume summary and experience bullet points to echo terms used in this job description.")

    return recs
