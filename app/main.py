from fastapi import FastAPI
from app.api import auth, vm
from app.db.database import engine
from app.db.models import Base
from app.core.logger import logger
import random
from app.db.database import SessionLocal
from app.db.models import VM

app = FastAPI(title="VM Manager API")

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def seed_data():
    db = SessionLocal()

    if db.query(VM).count() > 0:
        db.close()
        return

    logger.info("Seeding initial VM data")

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


app.include_router(auth.router)
app.include_router(vm.router)


@app.get("/")
def health():
    return {"message": "API is running"}