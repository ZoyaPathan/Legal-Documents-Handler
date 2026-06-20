from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.database import get_db
from app.models.user import User

from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_SECRET_KEY,
    ALGORITHM
)

from app.auth.dependencies import (
    get_current_user
)

router = APIRouter(
    tags=["Authentication"]
)



@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def signup(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(
            data.password
        ),
        role=data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data:
    OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user.email,
        user.role
    )

    refresh_token = create_refresh_token(
        user.email
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.get("/me")
def get_me(
    current_user=Depends(
        get_current_user
    )
):
    return current_user



@router.post(
    "/refresh",
    response_model=Token
)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            refresh_token,
            REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_access_token = create_access_token(
        user.email,
        user.role
    )

    new_refresh_token = create_refresh_token(
        user.email
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }