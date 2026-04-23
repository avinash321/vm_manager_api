from fastapi import APIRouter, Depends, Request
from app.core.redis_ratelimiter import limiter
from sqlalchemy.orm import Session
from app.schemas.schemas import VMCreate
from app.services.vm_service import *
from app.utils.security import verify_token
from app.api.deps import get_db

router = APIRouter()


@router.get("/vms")
@limiter.limit("5/minute")
def get_vms(request: Request, db: Session = Depends(get_db), user=Depends(verify_token)):
    return get_all_vms(db)


@router.post("/vms")
@limiter.limit("5/minute")
def create(request: Request, vm: VMCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    return create_vm(db, vm)


@router.get("/vms/{vm_id}")
@limiter.limit("5/minute")
def get(request: Request, vm_id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    return get_vm(db, vm_id)


@router.put("/vms/{vm_id}")
@limiter.limit("5/minute")
def update(request: Request, vm_id: int, vm: VMCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    return update_vm(db, vm_id, vm)


@router.delete("/vms/{vm_id}")
@limiter.limit("5/minute")
def delete(request: Request, vm_id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    return delete_vm(db, vm_id)