import json

from backend.models.game import DifficultyLevel
from backend.schemas.audio import AudioFeatures, TimeDomainFeatures, SpectralFeatures, PerceptualFeatures, RhythmFeatures, QualityFeatures
from backend.models.audio import AudioAnalytics

EASY_FEATURES = {
    # Time domain - basic signal energy
    "rms_energy","zcr",
    # Rhythm - most obvious music discriminator
    "tempo_bpm","tempo_confidence","beat_strength","onset_density",
    # Quality - intuitive noise/silence indicators
    "snr_db","dynamic_range_db","silence_ratio",
}

MEDIUM_FEATURES = {
    # Time domain - needs envelope/dynamics understanding
    "crest_factor","attack_time_ms",
    # Spectral shape - requires knowing frequency distribution
    "spectral_centroid","spectral_bandwidth","spectral_rolloff","spectral_flatness","spectral_flux",
    # Perceptual stats - summarized MFCCs are approachable
    "mfcc_mean","mel_stats_mean","mel_stats_std",
    # Quality - technical but single-value
    "clipping_ratio","thd_percent",
}

HARD_FEATURES = {
    # Time domain - periodicity analysis
    "autocorr",
    # Spectral - multi-band contrast requires experience
    "spectral_contrast",
    # Perceptual - raw arrays + variance, needs coefficient literacy
    "mfcc","mfcc_variance",
    # Harmony/tonality - music theory + DSP overlap
    "chroma","tonnetz",
}

ALL_FEATURES = EASY_FEATURES | MEDIUM_FEATURES | HARD_FEATURES

HINTS_BY_DIFFICULTY = {
    DifficultyLevel.easy:   {"count": 0, "order": []},
    DifficultyLevel.medium: {"count": 1, "order": ["easy", "easy"]},
    DifficultyLevel.hard:   {"count": 2, "order": ["medium", "easy"]},
}

ALL_FEATURES = EASY_FEATURES | MEDIUM_FEATURES | HARD_FEATURES

def get_initial_features(difficulty: DifficultyLevel) -> set:
    if difficulty == DifficultyLevel.easy:
        return ALL_FEATURES
    if difficulty == DifficultyLevel.medium:
        return HARD_FEATURES | MEDIUM_FEATURES
    return HARD_FEATURES

def get_hint_feature(difficulty: DifficultyLevel, hint_index: int) -> str:
    """Returns which tier to unlock for the nth hint"""
    order = HINTS_BY_DIFFICULTY[difficulty]["order"]
    if hint_index >= len(order):
        return None
    return order[hint_index]  # "hard", "medium", or "easy"

def filter_analytics(analytics: dict, visible_features: set) -> dict:
    return {k: v for k, v in analytics.items() if k in visible_features}

def serialize_features(analytics: AudioAnalytics, visible_features: set) -> AudioFeatures:
    """
    Converts ORM row to grouped AudioFeatures schema.
    Only includes fields present in visible_features, rest are None.
    """
    
    def pick(field: str):
        return getattr(analytics, field) if field in visible_features else None

    return AudioFeatures(
        time_domain=TimeDomainFeatures(
            rms_energy=pick("rms_energy"),
            zcr=pick("zcr"),
            crest_factor=pick("crest_factor"),
            attack_time_ms=pick("attack_time_ms"),
            autocorr=pick("autocorr"),
        ),
        spectral=SpectralFeatures(
            spectral_centroid=pick("spectral_centroid"),
            spectral_bandwidth=pick("spectral_bandwidth"),
            spectral_rolloff=pick("spectral_rolloff"),
            spectral_flatness=pick("spectral_flatness"),
            spectral_flux=pick("spectral_flux"),
            spectral_contrast=pick("spectral_contrast"),
        ),
        perceptual=PerceptualFeatures(
            mfcc=pick("mfcc"),
            mfcc_mean=parse_jsonb(pick("mfcc_mean")),
            mfcc_variance=parse_jsonb(pick("mfcc_variance")),
            mel_stats_mean=parse_jsonb(pick("mel_stats_mean")),
            mel_stats_std=pick("mel_stats_std"),
            chroma=pick("chroma"),
            tonnetz=pick("tonnetz"),
        ),
        rhythm=RhythmFeatures(
            tempo_bpm=pick("tempo_bpm"),
            tempo_confidence=pick("tempo_confidence"),
            beat_strength=pick("beat_strength"),
            onset_density=pick("onset_density"),
        ),
        quality=QualityFeatures(
            snr_db=pick("snr_db"),
            dynamic_range_db=pick("dynamic_range_db"),
            silence_ratio=pick("silence_ratio"),
            clipping_ratio=pick("clipping_ratio"),
            thd_percent=pick("thd_percent"),
        ),
    )

def parse_jsonb(value):
    if value is None:
        return None
    if isinstance(value, str):
        return json.loads(value)
    return value  # already a list