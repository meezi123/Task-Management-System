from sqlalchemy import Column, Integer, String, Enum, DateTime
from database import Base
from datetime import datetime
import enum

# Enum for status
class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"
class priorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
# Task table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    priority=Column(Enum(priorityEnum), default=priorityEnum.medium)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
