from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import VM
from app.core.logger import logger
from app.tasks.email_tasks import send_email_task
from app.core.config import EMAIL_TO_SENT

# ✅ Cache imports
from app.core.redis_cache import get_cache, set_cache, delete_cache


# =========================
# 🔧 Helper: Serializer
# =========================
def serialize_vm(vm: VM):
    return {
        "id": vm.id,
        "name": vm.name,
        "status": vm.status,
        "cpu": vm.cpu,
        "memory": vm.memory,
        "os": vm.os,
        "region": vm.region,
        "owner": vm.owner
    }

# =========================
# 📥 GET ALL VMs (Cached)
# =========================
def get_all_vms(db: Session):
    cache_key = "vm:list"

    # ✅ 1. Check cache
    cached_data = get_cache(cache_key)
    if cached_data:
        logger.info("Cache HIT for VM list")
        return cached_data

    logger.info("Cache MISS for VM list")

    # ✅ 2. Fetch from DB
    vms = db.query(VM).all()

    vm_list = [serialize_vm(vm) for vm in vms]

    # ✅ 3. Store in cache
    set_cache(cache_key, vm_list, ttl=300)

    return vm_list


# =========================
# 📥 GET SINGLE VM (Cached)
# =========================
def get_vm(db: Session, vm_id: int):
    cache_key = f"vm:{vm_id}"

    # ✅ 1. Check cache
    cached_vm = get_cache(cache_key)
    if cached_vm:
        logger.info("Cache HIT for VM: %s", vm_id)
        return cached_vm

    logger.info("Cache MISS for VM: %s", vm_id)

    # ✅ 2. Fetch from DB
    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        logger.warning("VM not found: %s", vm_id)
        raise HTTPException(status_code=404, detail="VM not found")

    vm_data = serialize_vm(vm)

    # ✅ 3. Store in cache
    set_cache(cache_key, vm_data, ttl=300)

    return vm_data


# =========================
# ➕ CREATE VM
# =========================
def create_vm(db: Session, vm_data):
    logger.info("Creating VM: %s", vm_data.name)

    vm = VM(**vm_data.dict())
    db.add(vm)
    db.commit()
    db.refresh(vm)

    # ✅ Serialize
    vm_dict = serialize_vm(vm)

    # ✅ Cache this VM
    set_cache(f"vm:{vm.id}", vm_dict, ttl=300)

    # ❗ Invalidate VM list cache
    delete_cache("vm:list")

    # async email
    send_email_task.delay(EMAIL_TO_SENT, vm_data.name)
    logger.info("VM Creation - Mail task sent")

    return vm_dict


# =========================
# ✏️ UPDATE VM
# =========================
def update_vm(db: Session, vm_id: int, vm_data):
    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")

    for key, value in vm_data.dict().items():
        setattr(vm, key, value)

    db.commit()
    db.refresh(vm)

    vm_dict = serialize_vm(vm)

    # ❗ Invalidate cache
    delete_cache(f"vm:{vm_id}")
    delete_cache("vm:list")

    logger.info("VM updated: %s", vm_id)

    return vm_dict


# =========================
# ❌ DELETE VM
# =========================
def delete_vm(db: Session, vm_id: int):
    vm = db.query(VM).filter(VM.id == vm_id).first()

    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")

    db.delete(vm)
    db.commit()

    # ❗ Invalidate cache
    delete_cache(f"vm:{vm_id}")
    delete_cache("vm:list")

    logger.info("VM deleted: %s", vm_id)

    return {"message": "VM deleted successfully"}