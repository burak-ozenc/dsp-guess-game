from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.routers import sessions, audio

app = FastAPI(title="DSP Game")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8001",
    "http://localhost:8002",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])