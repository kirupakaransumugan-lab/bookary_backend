from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import User
from app.schemas.auth import LibrarianCreate, UserCreate, UserResponse
from app.auth.security import (
    create_access_token,
    get_current_user,
    hash_password,
    require_admin,
    verify_password,
)

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
        role="member"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/create-librarian",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_librarian(
    user: LibrarianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
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
        role="librarian",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not existing_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.id,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
