from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class APIKey(Base):
    __tablename__ = "api_keys"

    id           = Column(Integer, primary_key=True, index=True)
    api_id       = Column(Integer, ForeignKey("apis.id", ondelete="CASCADE"), nullable=False)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key_value    = Column(String(64), unique=True, nullable=False, index=True)
    name         = Column(String(100), nullable=True)
    status       = Column(Enum("active", "revoked", "expired"), default="active")
    expires_at   = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    api   = relationship("API",  back_populates="keys")
    owner = relationship("User", back_populates="api_keys")