from pydantic import BaseModel, EmailStr


class AuthorCreate(BaseModel):
    name: str
    email: EmailStr
    country: str


class AuthorUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    country: str | None = None


class AuthorResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    country: str

    model_config = {
        "from_attributes": True
    }