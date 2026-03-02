import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# after routers are registered
if os.path.exists("static"):
    app.mount("/backend", app)   # keep API under /backend
    app.mount("/frontend", StaticFiles(directory="static", html=True), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        return FileResponse("static/index.html")