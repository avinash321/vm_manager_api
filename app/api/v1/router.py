
from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.vm import router as vm_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(vm_router)