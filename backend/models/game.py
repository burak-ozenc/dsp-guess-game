import uuid
import enum
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, SmallInteger, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from backend.database import Base

class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class GameSession(Base):
    __tablename__ = "game_sessions"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_file_id   = Column(UUID(as_uuid=True), ForeignKey("audio_files.id"), nullable=False)
    difficulty      = Column(Enum(DifficultyLevel, name="difficulty_level"), nullable=False)
    hints_used      = Column(SmallInteger, default=0)
    hints_remaining = Column(SmallInteger, nullable=False)
    user_answer     = Column(String)
    correct         = Column(Boolean)
    score           = Column(Integer)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    answered_at     = Column(DateTime(timezone=True))