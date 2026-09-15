from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas.books import BookCreate, BookUpdate, BookResponse


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# Get all books
@router.get(
    "/",
    response_model=list[BookResponse]
)
def get_books(
    category: str | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Book)

    # Filter by category
    if category is not None:
        query = query.filter(Book.category.ilike(category))

    # Filter by maximum price
    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    return query.all()


# Get a specific book
@router.get(
    "/{book_id}",
    response_model=BookResponse
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# Create a new book
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):

    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        category=book.category,
        available=book.available
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# Update a book
@router.put(
    "/{book_id}",
    response_model=BookResponse
)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db)
):

    selected_book = db.query(Book).filter(Book.id == book_id).first()

    if selected_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    update_data = book.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(selected_book, field, value)

    db.commit()
    db.refresh(selected_book)

    return selected_book


# Delete a book
@router.delete(
    "/{book_id}"
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }