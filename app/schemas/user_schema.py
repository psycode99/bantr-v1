from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    first_name: str
    last_name: str | None = None
    email: EmailStr
    profile_pic: str | None = None
    country: str | None = None
    fav_team: str | None = None


class UserResp(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str | None = None
    email: EmailStr
    profile_pic: str | None = None
    country: str | None = None
    fav_team: str | None = None
    created_at: datetime