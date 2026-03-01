from backend.models.game import DifficultyLevel
from backend.schemas.audio import AudioFeatures, TimeDomainFeatures, SpectralFeatures, PerceptualFeatures, RhythmFeatures, QualityFeatures
from backend.models.audio import AudioAnalytics

EASY_FEATURES = {
    "rms_energy", "zcr", "crest_factor", "snr_db",
    "dynamic_range_db", "silence_ratio"
}

MEDIUM_FEATURES = {
    "attack_time_ms", "spectral_centroid", "spectral_bandwidth",
    "spectral_rolloff", "spectral_flatness", "spectral_flux",
    "spectral_contrast", "mfcc_mean", "onset_density", "clipping_ratio"
}

HARD_FEATURES = {
    "autocorr", "mfcc", "mfcc_variance", "mel_stats_mean", "mel_stats_std",
    "chroma", "tonnetz", "tempo_bpm", "tempo_confidence",
    "beat_strength", "thd_percent"
}

HINTS_BY_DIFFICULTY = {
    DifficultyLevel.easy:   {"count": 0, "order": []},
    DifficultyLevel.medium: {"count": 2, "order": ["hard", "hard"]},
    DifficultyLevel.hard:   {"count": 5, "order": ["hard", "hard", "hard", "medium", "easy"]},
}

def get_initial_features(difficulty: DifficultyLevel) -> set:
    if difficulty == DifficultyLevel.easy:
        return EASY_FEATURES
    if difficulty == DifficultyLevel.medium:
        return EASY_FEATURES | MEDIUM_FEATURES
    return set()  # hard starts with nothing

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
            mfcc_mean=pick("mfcc_mean"),
            mfcc_variance=pick("mfcc_variance"),
            mel_stats_mean=pick("mel_stats_mean"),
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