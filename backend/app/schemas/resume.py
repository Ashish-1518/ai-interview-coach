from typing import Any

from pydantic import BaseModel


class ParsedResumeData(BaseModel):
    name: str | None = None
    emails: list[str] = []
    phone_numbers: list[str] = []
    skills: list[str] = []
    education: list[str] = []
    projects: list[str] = []
    experience: list[str] = []
    certifications: list[str] = []
    achievements: list[str] = []


class ResumeResponse(BaseModel):
    id: str
    original_filename: str
    content_type: str
    size_bytes: int
    parsed_data: dict[str, Any]
    parse_method: str

    model_config = {"from_attributes": True}


class ResumeDetailResponse(ResumeResponse):
    raw_text_preview: str
