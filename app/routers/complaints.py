from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.dependencies import get_current_user

from app.models.complaint import Complaint
from app.models.user import User

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintOut
)

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


@router.post(
    "/",
    response_model=ComplaintOut
)
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    complaint = Complaint(
        client_id=user.id,
        title=data.title,
        description=data.description,
        category=data.category,
        urgency=data.urgency,
        preferred_lawyer_id=data.preferred_lawyer_id
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


@router.get(
    "/",
    response_model=list[ComplaintOut]
)
def get_complaints(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    complaints = db.query(Complaint).filter(
        Complaint.client_id == user.id
    ).all()

    return complaints


@router.get(
    "/{complaint_id}",
    response_model=ComplaintOut
)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.client_id == user.id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return complaint