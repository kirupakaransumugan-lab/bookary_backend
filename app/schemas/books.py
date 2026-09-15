from pydantic import BaseModel, Field  # 


class BookCreate(BaseModel):
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    price: float = Field(gt=0)
    category: str
    available: bool


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2)
    author: str | None = Field(default=None, min_length=2)
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    available: bool | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    category: str
    available: bool



    