import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.resume import Resume
from app.models.user import User
from app.services.resume_parser import extract_text_from_pdf, parse_resume_text

ALLOWED_RESUME_CONTENT_TYPES = {"application/pdf"}


class ResumeUploadError(Exception):
    """Raised when a resume upload is invalid or cannot be processed."""


def list_resumes_for_user(db: Session, user: User) -> list[Resume]:
    return list(db.scalars(select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc())))


def get_resume_for_user(db: Session, user: User, resume_id: str) -> Resume | None:
    return db.scalar(select(Resume).where(Resume.id == resume_id, Resume.user_id == user.id))


def save_and_parse_resume(db: Session, user: User, upload: UploadFile, settings: Settings) -> Resume:
    if upload.content_type not in ALLOWED_RESUME_CONTENT_TYPES:
        raise ResumeUploadError("Only PDF resumes are supported.")

    storage_dir = Path(settings.storage_dir) / "resumes" / user.id
    storage_dir.mkdir(parents=True, exist_ok=True)

    original_filename = Path(upload.filename or "resume.pdf").name
    stored_filename = f"{uuid.uuid4()}.pdf"
    destination = storage_dir / stored_filename

    size_bytes = _write_upload_with_limit(upload, destination, settings.max_resume_upload_size_bytes)
    raw_text = extract_text_from_pdf(destination)
    if not raw_text:
        destination.unlink(missing_ok=True)
        raise ResumeUploadError("Could not extract text from this PDF. Scanned image-only resumes are not supported yet.")

    parsed = parse_resume_text(raw_text)
    resume = Resume(
        user_id=user.id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(destination),
        content_type=upload.content_type or "application/pdf",
        size_bytes=size_bytes,
        raw_text=raw_text,
        parsed_data=parsed.model_dump(),
        parse_method="heuristic_v1",
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def _write_upload_with_limit(upload: UploadFile, destination: Path, max_size_bytes: int) -> int:
    size = 0
    try:
        with destination.open("wb") as output_file:
            while chunk := upload.file.read(1024 * 1024):
                size += len(chunk)
                if size > max_size_bytes:
                    raise ResumeUploadError("Resume file is too large.")
                output_file.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        upload.file.close()
    return size
