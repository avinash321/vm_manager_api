from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from jose import jwt, JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from pydantic import BaseModel
import random
import os

# -----------------------------
# CONFIG
# -----------------------------
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ph = PasswordHasher()
security = HTTPBearer()

# -----------------------------
# DB Setup (PostgreSQL Ready)
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for Render postgres:// issue
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # important for production
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# -----------------------------
# MODELS
# -----------------------------
class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    cpu = Column(Integer)
    memory = Column(Integer)
    os = Column(String)
    region = Column(String)
    owner = Column(String)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


# ⚠️ Keep for now (remove after Alembic)
Base.metadata.create_all(bind=engine)

# -----------------------------
# SCHEMAS
# -----------------------------
class VMCreate(BaseModel):
    name: str
    status: str
    cpu: int
    memory: int
    os: str
    region: str
    owner: str


class UserCreate(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


# -----------------------------
# APP
# -----------------------------
app = FastAPI(title="VM Manager API (PostgreSQL + JWT + Argon2)")

# -----------------------------
# UTILS
# -----------------------------
def hash_password(password: str):
    return ph.hash(password)


def verify_password(plain, hashed):
    try:
        ph.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -----------------------------
# DB SESSION
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# AUTH APIs
# -----------------------------
@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: LoginRequest):
    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.username})
    db.close()

    return {"access_token": token, "token_type": "bearer"}


# -----------------------------
# DUMMY DATA
# -----------------------------
def seed_data():
    db = SessionLocal()

    if db.query(VM).count() > 0:
        db.close()
        return

    statuses = ["running", "stopped"]
    oss = ["linux", "windows"]
    regions = ["india", "us-east", "europe"]
    owners = ["team-a", "team-b"]

    for i in range(1, 101):
        vm = VM(
            name=f"vm-{i}",
            status=random.choice(statuses),
            cpu=random.choice([1, 2, 4]),
            memory=random.choice([2, 4, 8]),
            os=random.choice(oss),
            region=random.choice(regions),
            owner=random.choice(owners),
            is_active=True
        )
        db.add(vm)

    db.commit()
    db.close()


seed_data()

# -----------------------------
# PROTECTED VM APIs
# -----------------------------
@app.get("/vms")
def get_vms(user=Depends(verify_token)):
    db = SessionLocal()
    vms = db.query(VM).all()
    db.close()
    return vms


@app.post("/vms")
def create_vm(vm: VMCreate, user=Depends(verify_token)):
    db = SessionLocal()

    new_vm = VM(**vm.dict())
    db.add(new_vm)
    db.commit()
    db.refresh(new_vm)
    db.close()

    return new_vm


@app.get("/vms/{vm_id}")
def get_vm(vm_id: int, user=Depends(verify_token)):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")

    db.close()
    return vm


@app.put("/vms/{vm_id}")
def update_vm(vm_id: int, updated_vm: VMCreate, user=Depends(verify_token)):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")

    for key, value in updated_vm.dict().items():
        setattr(vm, key, value)

    db.commit()
    db.refresh(vm)
    db.close()

    return vm


@app.delete("/vms/{vm_id}")
def delete_vm(vm_id: int, user=Depends(verify_token)):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")

    db.delete(vm)
    db.commit()
    db.close()

    return {"message": "VM deleted successfully"}


# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def health():
    return {"message": "API is running"}