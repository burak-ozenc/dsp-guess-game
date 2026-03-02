export type Difficulty = 'easy' | 'medium' | 'hard'

export interface TimeDomainFeatures {
  rms_energy: number[] | null
  zcr: number[] | null
  crest_factor: number | null
  attack_time_ms: number | null
  autocorr: number[] | null
}

export interface SpectralFeatures {
  spectral_centroid: number | null
  spectral_bandwidth: number | null
  spectral_rolloff: number | null
  spectral_flatness: number | null
  spectral_flux: number[] | null
  spectral_contrast: number[] | null
}

export interface PerceptualFeatures {
  mfcc: number[][] | null
  mfcc_mean: number[] | null
  mfcc_variance: number[] | null
  mel_stats_mean: number[] | null
  mel_stats_std: number[] | null
  chroma: number[] | null
  tonnetz: number[] | null
}

export interface RhythmFeatures {
  tempo_bpm: number | null
  tempo_confidence: number | null
  beat_strength: number | null
  onset_density: number | null
}

export interface QualityFeatures {
  snr_db: number | null
  dynamic_range_db: number | null
  silence_ratio: number | null
  clipping_ratio: number | null
  thd_percent: number | null
}

export interface AudioFeatures {
  time_domain: TimeDomainFeatures
  spectral: SpectralFeatures
  perceptual: PerceptualFeatures
  rhythm: RhythmFeatures
  quality: QualityFeatures
}

export interface StartSessionResponse {
  session_id: string
  difficulty: Difficulty
  hints_remaining: number
  features: AudioFeatures
}

export interface HintResponse {
  hints_remaining: number
  unlocked_tier: 'easy' | 'medium' | 'hard'
  features: AudioFeatures
}

export interface GuessResponse {
  correct: boolean
  correct_answer: string
  score: number
}

export interface RevealResponse {
  audio_url: string
  category: string
  subcategory: string | null
  score: number
  hints_used: number
  features: AudioFeatures
}
