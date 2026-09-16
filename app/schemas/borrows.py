from datetime import date

from pydantic import BaseModel


class BorrowCreate(BaseModel):
    member_id: str
    book_id: int
    borrowed: date
    due: date


class BorrowUpdate(BaseModel):
    borrowed: date | None = None
    due: date | None = None
    returned: date | None = None
    status: str | None = None


class BorrowResponse(BaseModel):
    id: str
    member_id: str
    book_id: int
    borrowed: date
    due: date
    returned: date | None
    status: str

    model_config = {
        "from_attributes": True
    }