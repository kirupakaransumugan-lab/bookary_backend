from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str

    model_config = {
        "from_attributes": True
    }