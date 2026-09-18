from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Member, User
from app.auth.security import get_current_user, require_librarian
from app.schemas.members import (
    MemberCreate,
    MemberUpdate,
    MemberResponse
)


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.get("/")
def get_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    
    return db.query(Member).all()


@router.get(
    "/{member_id}",
    response_model=MemberResponse
)
def get_member(
    member_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED
)
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    last_member = (
        db.query(Member)
        .order_by(Member.id.desc())
        .first()
    )

    if last_member:
        last_number = int(last_member.id.split("-")[1])
        new_number = last_number + 1
    else:
        new_number = 1

    new_member = Member(
        id=f"mem-{new_number}",
        name=member.name,
        email=member.email,
        phone=member.phone,
        status=member.status,
        joined=member.joined
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


@router.put(
    "/{member_id}",
    response_model=MemberResponse
)
def update_member(
    member_id: str,
    member: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    selected_member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if selected_member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    update_data = member.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(selected_member, field, value)

    db.commit()
    db.refresh(selected_member)

    return selected_member


@router.delete(
    "/{member_id}"
)
def delete_member(
    member_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully"
    }