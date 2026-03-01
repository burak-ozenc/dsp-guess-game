from fastapi import FastAPI
from backend.routers import sessions, audio

app = FastAPI(title="DSP Game")

app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])