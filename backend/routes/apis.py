from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from utils.dependencies import require_owner
from schemas.api import APICreate, APIResponse, APIKeyCreate, APIKeyResponse
from controllers.api_controller import (
    create_api, list_apis, delete_api,
    generate_key, list_keys, revoke_key, rotate_key
)
from models.user import User

router = APIRouter(prefix="/apis", tags=["API Management"])

@router.post("/", response_model=APIResponse, status_code=201)
def create(data: APICreate, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return create_api(data, current_user, db)

@router.get("/", response_model=list[APIResponse])
def list_my_apis(current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return list_apis(current_user, db)

@router.delete("/{api_id}")
def delete(api_id: int, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return delete_api(api_id, current_user, db)

@router.post("/{api_id}/keys", response_model=APIKeyResponse, status_code=201)
def generate(api_id: int, data: APIKeyCreate, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return generate_key(api_id, data, current_user, db)

@router.get("/{api_id}/keys", response_model=list[APIKeyResponse])
def list_api_keys(api_id: int, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return list_keys(api_id, current_user, db)

@router.patch("/keys/{key_id}/revoke")
def revoke(key_id: int, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return revoke_key(key_id, current_user, db)

@router.post("/keys/{key_id}/rotate", response_model=APIKeyResponse)
def rotate(key_id: int, current_user: User = Depends(require_owner), db: Session = Depends(get_db)):
    return rotate_key(key_id, current_user, db)