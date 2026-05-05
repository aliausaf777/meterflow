from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=False,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

mongo_client = AsyncIOMotorClient(
    settings.MONGO_URL,
    tlsAllowInvalidCertificates=True
)
mongo_db = mongo_client[settings.MONGO_DB]
usage_logs = mongo_db["usage_logs"]

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)