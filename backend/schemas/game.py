from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.models.game import DifficultyLevel
from backend.schemas.audio import AudioFeatures

# ── Requests ───────────────────────────────────────────────────────────

class StartSessionRequest(BaseModel):
    difficulty: DifficultyLevel

class GuessRequest(BaseModel):
    answer: str

# ── Responses ──────────────────────────────────────────────────────────

class StartSessionResponse(BaseModel):
    session_id:      UUID
    difficulty:      DifficultyLevel
    hints_remaining: int
    features:        AudioFeatures

class HintResponse(BaseModel):
    hints_remaining: int
    unlocked_tier:   str              # "easy" | "medium" | "hard"
    features:        AudioFeatures    # only the newly unlocked tier's features

class GuessResponse(BaseModel):
    correct:         bool
    correct_answer:  str
    score:           int

class RevealResponse(BaseModel):
    audio_url:   str
    category:    str
    subcategory: Optional[str]
    score:       int
    hints_used:  int
    features:    AudioFeatures        # full feature set