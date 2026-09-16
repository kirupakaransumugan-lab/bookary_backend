from datetime import date

from pydantic import BaseModel, EmailStr


class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    status: str = "Active"
    joined: date


class MemberUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    status: str | None = None
    joined: date | None = None


class MemberResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    status: str
    joined: date

    model_config = {
        "from_attributes": True
    }