from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import VM
from app.core.logger import logger


def get_all_vms(db: Session):
    logger.info("Fetching all VMs")
    return db.query(VM).all()


def create_vm(db: Session, vm_data):
    logger.info("Creating VM: %s", vm_data.name)

    vm = VM(**vm_data.dict())
    db.add(vm)
    db.commit()
    db.refresh(vm)

    return vm


def get_vm(db: Session, vm_id: int):
    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        logger.warning("VM not found: %s", vm_id)
        raise HTTPException(status_code=404, detail="VM not found")

    return vm


def update_vm(db: Session, vm_id: int, vm_data):
    vm = get_vm(db, vm_id)

    for key, value in vm_data.dict().items():
        setattr(vm, key, value)

    db.commit()
    db.refresh(vm)

    logger.info("VM updated: %s", vm_id)
    return vm


def delete_vm(db: Session, vm_id: int):
    vm = get_vm(db, vm_id)

    db.delete(vm)
    db.commit()

    logger.info("VM deleted: %s", vm_id)
    return {"message": "VM deleted successfully"}