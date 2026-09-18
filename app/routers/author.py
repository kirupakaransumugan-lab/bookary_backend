from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Author, User
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.auth.security import get_current_user, require_librarian


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


# Get all authors
@router.get(
    "/",
    response_model=list[AuthorResponse]
)
def get_authors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Author).all()


# Get one author
@router.get(
    "/{author_id}",
    response_model=AuthorResponse
)
def get_author(
    author_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    author = db.query(Author).filter(
        Author.id == author_id
    ).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author


# Create author
@router.post(
    "/",
    response_model=AuthorResponse
)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    last_author = (
        db.query(Author)
        .order_by(Author.id.desc())
        .first()
    )

    if last_author:
        last_number = int(last_author.id.split("-")[1])
        new_number = last_number + 1
    else:
        new_number = 1

    new_author = Author(
        id=f"auth-{new_number}",
        name=author.name,
        email=author.email,
        country=author.country
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author



# Update author
@router.put(
    "/{author_id}",
    response_model=AuthorResponse
)
def update_author(
    author_id: str,
    author: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    # your existing update code
    selected_author = db.query(Author).filter(
        Author.id == author_id
    ).first()

    if selected_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    update_data = author.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(selected_author, field, value)

    db.commit()
    db.refresh(selected_author)

    return selected_author


# Delete author
@router.delete("/{author_id}")
def delete_author(
    author_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    author = db.query(Author).filter(
        Author.id == author_id
    ).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    db.delete(author)
    db.commit()

    return {
        "message": "Author deleted successfully"
    }