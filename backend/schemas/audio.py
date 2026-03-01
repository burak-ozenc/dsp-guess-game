from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# ── Features ──────────────────────────────────────────────────────────

class TimeDomainFeatures(BaseModel):
    rms_energy:     Optional[List[float]] = None
    zcr:            Optional[List[float]] = None
    crest_factor:   Optional[float] = None
    attack_time_ms: Optional[float] = None
    autocorr:       Optional[List[float]] = None

class SpectralFeatures(BaseModel):
    spectral_centroid:  Optional[float] = None
    spectral_bandwidth: Optional[float] = None
    spectral_rolloff:   Optional[float] = None
    spectral_flatness:  Optional[float] = None
    spectral_flux:      Optional[List[float]] = None
    spectral_contrast:  Optional[List[float]] = None

class PerceptualFeatures(BaseModel):
    mfcc:           Optional[List[List[float]]] = None
    mfcc_mean:      Optional[List[float]] = None
    mfcc_variance:  Optional[List[float]] = None
    mel_stats_mean: Optional[List[float]] = None
    mel_stats_std:  Optional[List[float]] = None
    chroma:         Optional[List[float]] = None
    tonnetz:        Optional[List[float]] = None

class RhythmFeatures(BaseModel):
    tempo_bpm:        Optional[float] = None
    tempo_confidence: Optional[float] = None
    beat_strength:    Optional[float] = None
    onset_density:    Optional[float] = None

class QualityFeatures(BaseModel):
    snr_db:          Optional[float] = None
    dynamic_range_db: Optional[float] = None
    silence_ratio:   Optional[float] = None
    clipping_ratio:  Optional[float] = None
    thd_percent:     Optional[float] = None

class AudioFeatures(BaseModel):
    """
    Grouped feature response. Fields are None when not yet unlocked
    by difficulty or hint system.
    """
    time_domain: TimeDomainFeatures
    spectral:    SpectralFeatures
    perceptual:  PerceptualFeatures
    rhythm:      RhythmFeatures
    quality:     QualityFeatures

# ── Audio File ─────────────────────────────────────────────────────────

class AudioFileResponse(BaseModel):
    id:          UUID
    category:    str
    subcategory: Optional[str]
    duration_ms: Optional[int]
    sample_rate: Optional[int]

    model_config = {"from_attributes": True}  # allows ORM → Pydantic conversion