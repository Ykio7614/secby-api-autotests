from typing import Any

from pydantic import BaseModel


class ProfileRole(BaseModel):
    id: int
    name: str
    description: str


class AccountProfile(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    profile_id: int | None
    is_active: bool
    created_at: str
    updated_at: str
    role: ProfileRole
    profile: dict[str, Any] | None = None


class UserProfileResponse(BaseModel):
    message: str
    profile: AccountProfile
