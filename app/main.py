from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.core.redis_ratelimiter import (
    limiter,
    rate_limit_exceeded_handler
)
from app.api import auth, vm

from app.db.database import engine
from app.db.models import Base
from app.core.logger import logger
import random
from app.db.database import SessionLocal
from app.db.models import VM
from app.core.celery_worker_app import celery_app
from app.api.v1.router import router as v1_router

app = FastAPI(title="VM Manager API")

# Attach limiter to app
app.state.limiter = limiter

# Middleware
app.add_middleware(SlowAPIMiddleware)

# Exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

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


@app.get("/")
def health():
    return {"message": "API is running"}



# Register versions
app.include_router(v1_router, prefix="/api/v1")





