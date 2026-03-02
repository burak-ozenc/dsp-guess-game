import uuid
from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, ForeignKey, SmallInteger, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import Text
from backend.database import Base
import enum


class ProcessStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class AudioSource(Base):
    __tablename__ = "audio_sources"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_source_name = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_source_id = Column(UUID(as_uuid=True), ForeignKey("audio_sources.id"), nullable=False)
    s3_key = Column(String)
    s3_bucket = Column(String)
    duration_ms = Column(Integer)
    sample_rate = Column(Integer)
    file_path = Column(Text, nullable=False, unique=True)
    file_size = Column(BigInteger, nullable=False)
    file_name = Column(String, nullable=False)
    file_hash = Column(String, nullable=False, unique=True)
    status = Column(Enum(ProcessStatus, name="process_status"), default=ProcessStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))


class AudioAnalytics(Base):
    __tablename__ = "audio_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_source_id = Column(UUID(as_uuid=True), ForeignKey("audio_sources.id"), nullable=False)
    audio_file_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id"), nullable=False)
    source_type = Column(Text, nullable=False)

    # Analysis params
    hop_length = Column(Integer)
    n_fft = Column(Integer)
    n_mfcc = Column(SmallInteger)

    # Time Domain
    rms_energy = Column(JSONB)
    zcr = Column(JSONB)
    crest_factor = Column(Float)
    attack_time_ms = Column(Float)
    autocorr = Column(JSONB)

    # Spectral
    spectral_centroid = Column(Float)
    spectral_bandwidth = Column(Float)
    spectral_rolloff = Column(Float)
    spectral_flatness = Column(Float)
    spectral_flux = Column(JSONB)
    spectral_contrast = Column(JSONB)

    # Perceptual
    mfcc = Column(JSONB)
    mfcc_mean = Column(JSONB)
    mfcc_variance = Column(JSONB)
    mel_stats_mean = Column(JSONB)
    mel_stats_std = Column(JSONB)
    chroma = Column(JSONB)
    tonnetz = Column(JSONB)

    # Rhythm
    tempo_bpm = Column(Float)
    tempo_confidence = Column(Float)
    beat_strength = Column(Float)
    onset_density = Column(Float)

    # Quality
    snr_db = Column(Float)
    silence_ratio = Column(Float)
    clipping_ratio = Column(Float)
    dynamic_range_db = Column(Float)
    thd_percent = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
