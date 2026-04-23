from fastapi import APIRouter, Depends, Request
from app.core.redis_ratelimiter import limiter
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, LoginRequest
from app.services.auth_service import register_user, login_user
from app.api.deps import get_db

router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user.username, user.password)


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, user.username, user.password)