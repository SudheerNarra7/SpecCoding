from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class UserStatus(enum.Enum):
    pending = "pending"
    verified = "verified"
    suspended = "suspended"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(Enum(UserStatus), default=UserStatus.pending)
    verification_token = Column(String, unique=True)
    provider = Column(String, default="local")
    provider_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())