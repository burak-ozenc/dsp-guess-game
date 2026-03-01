from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.models.audio import AudioFile
from backend.models.game import GameSession
from backend.services.s3 import generate_presigned_url
import uuid

router = APIRouter()

@router.get("/{audio_id}/stream")
async def stream_audio(audio_id: uuid.UUID, session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Only accessible after a guess has been submitted.
    session_id is required to verify the user has answered.
    """
    session = await db.get(GameSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.correct is None:
        raise HTTPException(status_code=403, detail="Must submit a guess before accessing audio")
    if session.audio_file_id != audio_id:
        raise HTTPException(status_code=403, detail="Audio does not belong to this session")

    audio_file = await db.get(AudioFile, audio_id)
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")

    url = generate_presigned_url(audio_file.s3_bucket, audio_file.s3_key)
    return {"audio_url": url, "expires_in": 300}