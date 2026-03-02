FROM python:3.11-slim

# Install Node + ffmpeg
RUN apt-get update && apt-get install -y ffmpeg curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

WORKDIR /app

# Build frontend
COPY dsp-game/frontend/package.json dsp-game/frontend/package-lock.json ./frontend/
RUN cd frontend && npm ci

COPY dsp-game/ ./frontend/
RUN cd frontend && npm run build

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY . .

# Move built frontend to where FastAPI can serve it
RUN mv frontend/dist ./static

EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]