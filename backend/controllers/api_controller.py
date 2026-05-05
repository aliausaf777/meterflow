from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.api import API
from models.api_key import APIKey
from models.user import User
from schemas.api import APICreate, APIKeyCreate
from utils.keygen import generate_api_key

def create_api(data: APICreate, current_user: User, db: Session) -> API:
    new_api = API(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        base_url=data.base_url.rstrip("/"),
    )
    db.add(new_api)
    db.commit()
    db.refresh(new_api)
    return new_api

def list_apis(current_user: User, db: Session) -> list[API]:
    return db.query(API).filter(API.user_id == current_user.id).all()

def get_api_or_404(api_id: int, current_user: User, db: Session) -> API:
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    if api.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your API")
    return api

def delete_api(api_id: int, current_user: User, db: Session) -> dict:
    api = get_api_or_404(api_id, current_user, db)
    db.delete(api)
    db.commit()
    return {"message": f"API '{api.name}' deleted successfully"}

def generate_key(api_id: int, data: APIKeyCreate, current_user: User, db: Session) -> APIKey:
    api = get_api_or_404(api_id, current_user, db)
    new_key = APIKey(
        api_id=api.id,
        user_id=current_user.id,
        key_value=generate_api_key(),
        name=data.name,
        expires_at=data.expires_at,
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return new_key

def list_keys(api_id: int, current_user: User, db: Session) -> list[APIKey]:
    api = get_api_or_404(api_id, current_user, db)
    return db.query(APIKey).filter(APIKey.api_id == api.id).all()

def revoke_key(key_id: int, current_user: User, db: Session) -> dict:
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    api = db.query(API).filter(API.id == key.api_id).first()
    if api.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your API key")
    if key.status == "revoked":
        raise HTTPException(status_code=400, detail="Key already revoked")
    key.status = "revoked"
    db.commit()
    return {"message": f"Key '{key.key_value}' revoked"}

def rotate_key(key_id: int, current_user: User, db: Session) -> APIKey:
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    api = db.query(API).filter(API.id == key.api_id).first()
    if api.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your API key")
    key.status = "revoked"
    new_key = APIKey(
        api_id=key.api_id,
        user_id=current_user.id,
        key_value=generate_api_key(),
        name=f"{key.name} (rotated)" if key.name else None,
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return new_key