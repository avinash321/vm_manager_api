from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import User
from app.utils.security import hash_password, verify_password, create_token
from app.core.logger import logger


def register_user(db: Session, username: str, password: str):
    logger.info("Register attempt for user: %s", username)

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        logger.warning("User already exists: %s", username)
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=username,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()

    logger.info("User registered successfully: %s", username)
    return {"message": "User registered successfully"}


def login_user(db: Session, username: str, password: str):
    logger.info("Login attempt: %s", username)

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        logger.error("Invalid login for user: %s", username)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}