from pydantic import BaseModel, Field


class CandidateProfileBase(BaseModel):
    full_name: str | None = Field(default=None, max_length=120)
    target_role: str | None = Field(default=None, max_length=120)
    experience_level: str | None = Field(default=None, max_length=50)
    bio: str | None = Field(default=None, max_length=1000)


class CandidateProfileCreate(CandidateProfileBase):
    pass


class CandidateProfileUpdate(CandidateProfileBase):
    pass


class CandidateProfileResponse(CandidateProfileBase):
    id: str
    user_id: str

    model_config = {"from_attributes": True}
