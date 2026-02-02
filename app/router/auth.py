from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password
# from passlib.exc import PasswordSizeError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    pwd_bytes_len = len(payload.password.encode("utf-8"))

    if pwd_bytes_len > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password too long ({pwd_bytes_len} bytes; bcrypt limit is 72 bytes)"
        )

    try:
        hashed = hash_password(payload.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long (bcrypt limit is 72 bytes)"
        )

    user = User(email=payload.email, hashed_password=hashed)
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    db.refresh(user)
    return user

