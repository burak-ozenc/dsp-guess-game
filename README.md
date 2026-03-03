---
title: DSP Guess The Sound Source
emoji: 🎵
colorFrom: purple
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# DSP - Guess The Sound Source Game
Purpose is to guess the source sound type(music, noise, speech) from given analytics, based on time, spectral, perceptual, rhythm and quality features of already processes audios.
# Signal.Guess 🎛️

An audio classification game built around DSP literacy. No waveforms, no playback — just raw signal features. Analyze the numbers, make your guess.

## How It Works

A random audio sample is picked from the dataset. Its DSP features are displayed grouped by category. You try to identify the sound type from the signal characteristics alone. After guessing, the audio is revealed.

## Difficulty

| Level | Features Shown | Hints                         |
|---|---|-------------------------------|
| Easy | All features visible | None                          |
| Medium | Time domain + spectral | 1 hints                       |
| Hard | Nothing — start blind | 2 hints |

Hints in hard mode unlock from the most complex features first, so early hints are still challenging to interpret.

## Feature Groups

- **Time Domain** — RMS Energy, ZCR, Crest Factor, Attack Time, Autocorrelation
- **Frequency Domain** — Spectral Centroid, Bandwidth, Rolloff, Flatness, Flux, Contrast
- **Perceptual / Timbral** — MFCC, Chroma, Tonnetz, Mel Spectrogram Stats
- **Rhythm / Temporal** — Tempo, Beat Strength, Onset Density
- **Signal Quality** — SNR, Dynamic Range, Silence Ratio, Clipping Ratio

## Stack

**Frontend** — React + TypeScript + Vite + Tailwind CSS + Zustand

**Backend** — FastAPI + SQLAlchemy (async) + PostgreSQL (Neon)

**Pipeline** — Python + librosa + Prefect + FFmpeg

**Storage** — S3 for audio blobs

**Deployment** — Hugging Face Spaces (Docker)

## Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL=http://localhost:8000/api
npm run dev
```

## Environment Variables

```
DATABASE_URL=postgresql+asyncpg://...
S3_BUCKET=
S3_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

On Hugging Face Spaces, set these in the **Settings → Variables and Secrets** tab.

## Audio Pipeline

Audio files are preprocessed with FFmpeg before analysis — clipped to 30 seconds from the middle of the recording, converted to mono WAV at 16kHz. Features are extracted with librosa and stored in PostgreSQL as JSONB. Audio blobs are stored in S3 and served via presigned URLs after a guess is submitted.
To process start the process, set your **DATA_ROOT_PATH** and **CONNECTION_STRING** as is in .env.example and run command below.
You can also select bulk COPY size, file size to process, etc. from config file. 
```
python -m pipeline.pipeline.flow
```

## Project Structure

```
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   └── schemas/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── store/
│   │   ├── api/
│   │   └── types/
├── pipeline/
│   ├── dsp/
│   ├── ingestion/
│   ├── pipeline/
│   ├── schema/
│   ├── pipeline/
│   └── storage/
└── Dockerfile
```

## For Future Development
- Prefect flow needs to be configured. It created problem because we need to save the processed 30 sec files.
- Hints can be optimized better, now it depends on difficulty level, can be configured to reveal single field.
- 
