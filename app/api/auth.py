from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, LoginRequest
from app.services.auth_service import register_user, login_user
from app.api.deps import get_db

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user.username, user.password)


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, user.username, user.password)