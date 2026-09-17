from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.auth import UserCreate, UserResponse
from app.auth.security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    last_user = db.query(User).order_by(User.id.desc()).first()

    if last_user:
        last_number = int(last_user.id.split("-")[1])
        new_id = f"usr-{last_number + 1}"
    else:
        new_id = "usr-1"

    new_user = User(
        id=new_id,
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user