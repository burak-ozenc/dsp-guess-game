from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database import get_db
from backend.models.audio import AudioFile, AudioAnalytics, AudioSource
from backend.models.game import GameSession, DifficultyLevel
from backend.schemas.game import StartSessionRequest, GuessRequest
from backend.services.feature_filter import get_initial_features, filter_analytics, HINTS_BY_DIFFICULTY, HARD_FEATURES, \
    MEDIUM_FEATURES, EASY_FEATURES, get_hint_feature, serialize_features, ALL_FEATURES
from backend.services.scoring import calc_score
import random, uuid
from datetime import datetime, timezone

router = APIRouter()

@router.post("/")
async def start_session(difficulty: StartSessionRequest, db: AsyncSession = Depends(get_db)):
    print("Session starting")
    print("Difficulty:", difficulty.difficulty.value)
    # pick a random completed audio file
    result = await db.execute(
        select(AudioFile).where(AudioFile.status == "completed").order_by(func.random()).limit(1)
    )
    audio_file = result.scalar_one_or_none()
    print("audio file found", audio_file.audio_source_id)
    if not audio_file:
        raise HTTPException(status_code=404, detail="No audio samples available")
    
    print("Getting analytics")
    analytics = await db.execute(
        select(AudioAnalytics).where(AudioAnalytics.audio_file_id == audio_file.id)
    )
    analytics = analytics.scalar_one_or_none()
    print("analytics found")
    hints_config = HINTS_BY_DIFFICULTY[difficulty.difficulty.value]
    print("Creating Game Session")
    session = GameSession(
        audio_file_id=audio_file.id,
        difficulty=difficulty.difficulty.value,
        hints_remaining=hints_config["count"]
    )
    db.add(session)
    await db.commit()
    print("Session created")
    
    visible = get_initial_features(difficulty.difficulty)
    
    return {
        "session_id": session.id,
        "difficulty": difficulty.difficulty.value,
        "hints_remaining": session.hints_remaining,
        # "features": filter_analytics(analytics.__dict__, visible)
        "features": serialize_features(analytics, visible)
    }

@router.post("/{session_id}/hint")
async def use_hint(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    session = await db.get(GameSession, session_id)
    if not session:
        raise HTTPException(status_code=404)
    if session.hints_remaining <= 0:
        raise HTTPException(status_code=400, detail="No hints remaining")
    if session.correct is not None:
        raise HTTPException(status_code=400, detail="Session already answered")
    print('Getting analytics')
    analytics = await db.execute(
        select(AudioAnalytics).where(AudioAnalytics.audio_file_id == session.audio_file_id)
    )
    print('Got analytics')
    
    analytics = analytics.scalar_one()
    print('Get hint features')
    hint_tier = get_hint_feature(session.difficulty, session.hints_used)
    tier_features = {"hard": HARD_FEATURES, "medium": MEDIUM_FEATURES, "easy": EASY_FEATURES}[hint_tier]

    session.hints_used += 1
    session.hints_remaining -= 1
    await db.commit()
    
    print("Hint usage saved to database")
    
    return {
        "hints_remaining": session.hints_remaining,
        "unlocked_tier": hint_tier,
        # "features": filter_analytics(analytics.__dict__, tier_features)
        "features": serialize_features(analytics, tier_features)
    }

@router.post("/{session_id}/guess")
async def submit_guess(session_id: uuid.UUID, answer: GuessRequest, db: AsyncSession = Depends(get_db)):
    session = await db.get(GameSession, session_id)
    if not session:
        raise HTTPException(status_code=404)
    if session.correct is not None:
        raise HTTPException(status_code=400, detail="Already answered")

    audio_file = await db.get(AudioFile, session.audio_file_id)
    audio_source = await db.get(AudioSource, audio_file.audio_source_id)
    correct = answer.answer.lower() == audio_source.audio_source_name.lower()

    session.user_answer = answer.answer
    session.correct = correct
    session.answered_at = datetime.now(timezone.utc)
    session.score = calc_score(correct, session.difficulty, session.hints_used)
    await db.commit()

    return {
        "correct": correct,
        "correct_answer": audio_source.audio_source_name,
        "score": session.score
    }

@router.get("/{session_id}/reveal")
async def reveal(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    session = await db.get(GameSession, session_id)
    if not session or session.correct is None:
        raise HTTPException(status_code=403, detail="Must answer before reveal")

    from backend.services.s3 import generate_presigned_url
    audio_file = await db.get(AudioFile, session.audio_file_id)
    audio_source = await db.get(AudioSource, audio_file.audio_source_id)
    analytics = await db.execute(
        select(AudioAnalytics).where(AudioAnalytics.audio_file_id == session.audio_file_id)
    )
    analytics = analytics.scalar_one()

    return {
        "audio_url": generate_presigned_url(audio_file.s3_bucket, audio_file.s3_key),
        "category": audio_source.audio_source_name,
        "subcategory": audio_source.audio_source_name,
        # "all_features": analytics.__dict__
        "all_features": serialize_features(analytics, ALL_FEATURES)
    }

@router.get("/categories")
async def categories(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AudioSource))
    audio_sources = res.scalars().all()
    source_name_list = [s.audio_source_name for s in audio_sources]
    return source_name_list