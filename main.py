from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import random

# -----------------------------
# DB Setup
# -----------------------------
DATABASE_URL = "sqlite:///./vms.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# -----------------------------
# VM Model
# -----------------------------
class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)  # running, stopped
    cpu = Column(Integer)
    memory = Column(Integer)  # in GB
    os = Column(String, index=True)
    region = Column(String, index=True)
    owner = Column(String, index=True)
    is_active = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="VM Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Dummy Data Generator
# -----------------------------
def seed_data():
    db = SessionLocal()

    if db.query(VM).count() > 0:
        db.close()
        return

    statuses = ["running", "stopped"]
    oss = ["linux", "windows"]
    regions = ["us-east", "us-west", "india", "europe"]
    owners = ["team-a", "team-b", "team-c"]

    for i in range(1, 101):
        vm = VM(
            name=f"vm-{i}",
            status=random.choice(statuses),
            cpu=random.choice([1, 2, 4, 8]),
            memory=random.choice([2, 4, 8, 16]),
            os=random.choice(oss),
            region=random.choice(regions),
            owner=random.choice(owners),
            is_active=True,
        )
        db.add(vm)

    db.commit()
    db.close()


seed_data()


# -----------------------------
# CREATE VM
# -----------------------------
@app.post("/vms")
def create_vm(vm: dict):
    db = SessionLocal()

    new_vm = VM(**vm)
    db.add(new_vm)
    db.commit()
    db.refresh(new_vm)

    db.close()
    return new_vm


# -----------------------------
# GET ALL VMs (with filters)
# -----------------------------
@app.get("/vms")
def get_vms(
    status: str = None,
    os: str = None,
    region: str = None,
    owner: str = None,
    skip: int = 0,
    limit: int = 10,
):
    db = SessionLocal()

    query = db.query(VM)

    if status:
        query = query.filter(VM.status == status)
    if os:
        query = query.filter(VM.os == os)
    if region:
        query = query.filter(VM.region == region)
    if owner:
        query = query.filter(VM.owner == owner)

    vms = query.offset(skip).limit(limit).all()
    db.close()

    return vms


# -----------------------------
# GET VM BY ID
# -----------------------------
@app.get("/vms/{vm_id}")
def get_vm(vm_id: int):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        db.close()
        raise HTTPException(status_code=404, detail="VM not found")

    db.close()
    return vm


# -----------------------------
# UPDATE VM
# -----------------------------
@app.put("/vms/{vm_id}")
def update_vm(vm_id: int, updated_data: dict):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        db.close()
        raise HTTPException(status_code=404, detail="VM not found")

    for key, value in updated_data.items():
        setattr(vm, key, value)

    db.commit()
    db.refresh(vm)
    db.close()

    return vm


# -----------------------------
# DELETE VM
# -----------------------------
@app.delete("/vms/{vm_id}")
def delete_vm(vm_id: int):
    db = SessionLocal()

    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        db.close()
        raise HTTPException(status_code=404, detail="VM not found")

    db.delete(vm)
    db.commit()
    db.close()

    return {"message": "VM deleted successfully"}


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def health():
    return {"message": "VM Manager API is running"}