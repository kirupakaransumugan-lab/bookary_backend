from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category
from app.schemas.categories import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):

    return db.query(Category).all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):

    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    last_category = (
        db.query(Category)
        .order_by(Category.id.desc())
        .first()
    )

    if last_category:
        last_number = int(last_category.id.split("-")[1])
        new_number = last_number + 1
    else:
        new_number = 1

    new_category = Category(
        id=f"cat-{new_number}",
        name=category.name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: str,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):

    selected_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if selected_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    update_data = category.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(selected_category, field, value)

    db.commit()
    db.refresh(selected_category)

    return selected_category


@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db)
):

    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }