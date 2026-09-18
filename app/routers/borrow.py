from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Borrow, Book, Member, User
from app.auth.security import require_librarian
from app.schemas.borrows import (
    BorrowCreate,
    BorrowUpdate,
    BorrowResponse
)


router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)


@router.get(
    "/",
    response_model=list[BorrowResponse]
)
def get_borrows(
    db: Session = Depends(get_db)
):
    return db.query(Borrow).all()


@router.get(
    "/{borrow_id}",
    response_model=BorrowResponse
)
def get_borrow(
    borrow_id: str,
    db: Session = Depends(get_db)
):

    borrow = db.query(Borrow).filter(
        Borrow.id == borrow_id
    ).first()

    if borrow is None:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    return borrow


@router.post(
    "/",
    response_model=BorrowResponse
)
def create_borrow(
    borrow: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    member = db.query(Member).filter(
        Member.id == borrow.member_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    book = db.query(Book).filter(
        Book.id == borrow.book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if not book.available:
        raise HTTPException(
            status_code=400,
            detail="Book is not available"
        )

    last_borrow = (
        db.query(Borrow)
        .order_by(Borrow.id.desc())
        .first()
    )

    if last_borrow:
        last_number = int(last_borrow.id.split("-")[1])
        new_number = last_number + 1
    else:
        new_number = 1

    new_borrow = Borrow(
        id=f"brw-{new_number}",
        member_id=borrow.member_id,
        book_id=borrow.book_id,
        borrowed=borrow.borrowed,
        due=borrow.due,
        status="Borrowed"
    )

    book.available = False

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)

    return new_borrow


@router.put(
    "/{borrow_id}",
    response_model=BorrowResponse
)
def return_book(
    borrow_id: str,
    borrow: BorrowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    selected_borrow = db.query(Borrow).filter(
        Borrow.id == borrow_id
    ).first()

    if selected_borrow is None:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    update_data = borrow.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(selected_borrow, field, value)

    db.commit()
    db.refresh(selected_borrow)

    return selected_borrow


@router.delete(
    "/{borrow_id}"
)
def delete_borrow(
    borrow_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    borrow = db.query(Borrow).filter(
        Borrow.id == borrow_id
    ).first()

    if borrow is None:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    db.delete(borrow)
    db.commit()

    return {
        "message": "Borrow record deleted successfully"
    }