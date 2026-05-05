from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APICreate(BaseModel):
    name:        str
    description: Optional[str] = None
    base_url:    str

class APIResponse(BaseModel):
    id:          int
    user_id:     int
    name:        str
    description: Optional[str]
    base_url:    str
    is_active:   bool
    created_at:  datetime

    class Config:
        from_attributes = True

class APIKeyCreate(BaseModel):
    name:       Optional[str] = None
    expires_at: Optional[datetime] = None

class APIKeyResponse(BaseModel):
    id:          int
    api_id:      int
    key_value:   str
    name:        Optional[str]
    status:      str
    expires_at:  Optional[datetime]
    created_at:  datetime

    class Config:
        from_attributes = True