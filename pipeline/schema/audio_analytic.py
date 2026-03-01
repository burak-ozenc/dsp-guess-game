import uuid
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class AudioAnalytic:
    id: Optional[uuid.UUID] = None
    audio_file_id: Optional[uuid.UUID] = None
    audio_source_id: Optional[uuid.UUID] = None

    # Analysis params
    hop_length: Optional[int] = None
    n_fft: Optional[int] = None
    n_mfcc: Optional[int] = None

    # Time Domain
    rms_energy: Optional[List[float]] = None
    zcr: Optional[List[float]] = None
    crest_factor: Optional[float] = None
    attack_time_ms: Optional[float] = None
    autocorr: Optional[List[float]] = None

    # Spectral
    spectral_centroid: Optional[float] = None
    spectral_bandwidth: Optional[float] = None
    spectral_rolloff: Optional[float] = None
    spectral_flatness: Optional[float] = None
    spectral_flux: Optional[List[float]] = None
    spectral_contrast: Optional[List[float]] = None

    # Perceptual
    mfcc: Optional[List[List[float]]] = None
    mfcc_mean: Optional[List[float]] = None
    mfcc_variance: Optional[List[float]] = None
    mel_stats_mean: Optional[List[float]] = None
    mel_stats_std: Optional[List[float]] = None
    chroma: Optional[List[float]] = None
    tonnetz: Optional[List[float]] = None

    # Rhythm
    tempo_bpm: Optional[float] = None
    tempo_confidence: Optional[float] = None
    beat_strength: Optional[float] = None
    onset_density: Optional[float] = None

    # Quality
    snr_db: Optional[float] = None
    silence_ratio: Optional[float] = None
    clipping_ratio: Optional[float] = None
    dynamic_range_db: Optional[float] = None
    thd_percent: Optional[float] = None

    created_at: Optional[datetime] = None
    source_type: str = ""
