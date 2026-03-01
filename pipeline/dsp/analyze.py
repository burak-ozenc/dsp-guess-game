import librosa
import numpy as np

from config.config import config
from pipeline.schema.audio_analytic import AudioAnalytic


def analyze_audio(file_path: str) -> AudioAnalytic:
    """
    We will extract some features from given audio(path):
    
    """
    y, sr = librosa.load(file_path, sr=16000)  # standard sr across all data

    mfcc, mfcc_mean, mfcc_variance = calc_mfcc(audio=y, sr=sr)
    mel_spec_mean, mel_spec_std = calc_mel_spec(audio=y, sr=sr)
    tempo, tempo_confidence, beat_strength, onset_density = calc_rhythm_specs(audio=y, sr=sr)

    analytics = AudioAnalytic(
        hop_length=config.HOP_LENGTH,
        n_fft=config.N_FFT,
        n_mfcc=config.N_MFCC,
        # time domain
        rms_energy=calc_rms_energy(audio=y),
        zcr=calc_zcr(audio=y),
        crest_factor=calc_crest_factor(audio=y, sr=sr),
        attack_time_ms=calc_attack_time(audio=y, sr=sr),
        autocorr=calc_auto_correlation(audio=y),
        spectral_centroid=calc_spectral_centroid(audio=y, sr=sr),
        spectral_bandwidth=calc_spectral_bandwidth(audio=y, sr=sr),
        spectral_rolloff=calc_spectral_rolloff(audio=y, sr=sr),
        spectral_flatness=calc_spectral_flatness(audio=y),
        spectral_flux=calc_spectral_flux(audio=y, sr=sr),
        spectral_contrast=calc_spectral_contrast(audio=y, sr=sr),
        # perceptual
        mfcc=mfcc,
        mfcc_mean=mfcc_mean,
        mfcc_variance=mfcc_variance,
        mel_stats_std=mel_spec_std,
        mel_stats_mean=mel_spec_mean,
        chroma=calc_chromagram(audio=y, sr=sr),
        tonnetz=calc_tonnetz(audio=y, sr=sr),
        # Rhythm
        tempo_bpm=tempo,
        tempo_confidence=tempo_confidence,
        beat_strength=beat_strength,
        onset_density=onset_density,

        # quality
        snr_db=calc_snr(audio=y),
        silence_ratio=calc_silence_ratio(audio=y),
        clipping_ratio=calc_clipping_ratio(audio=y),
        dynamic_range_db=calc_dynamic_range(audio=y),
        # thd_percent=
    )

    return analytics


def calc_rms_energy(audio) -> [float]:
    """
    Calculate Root-Mean-Square of given audio
    """
    rms_energy = librosa.feature.rms(y=audio)[0]

    return rms_energy.tolist()


def calc_clipping_ratio(audio):
    threshold = 0.99
    clipped_samples = np.sum(np.abs(audio) >= threshold)
    clipping_ratio = clipped_samples / audio.size

    return safe_float(clipping_ratio)


def calc_zcr(audio) -> [float]:
    """
    Calculate how many times the audio waveform change singes 
    """
    zcr = librosa.feature.zero_crossing_rate(y=audio)[0]

    return zcr.tolist()


def calc_crest_factor(audio, sr):
    """
    Max amplitude / average of RMS of audio  
    """
    max_amplitude = np.max(np.abs(audio))

    return safe_float(max_amplitude / np.sqrt(np.mean(audio ** 2)))


# will study this one #TODO
def calc_attack_time(audio, sr):
    """
    Use RMS energy instead of raw amplitude
    More robust to noise
    """
    # Calculate RMS energy
    rms = librosa.feature.rms(
        y=audio,
        frame_length=int(0.02 * sr),  # 20ms frames
        hop_length=int(0.01 * sr)  # 10ms hop
    )[0]

    # Find onset and peak in RMS
    max_rms = np.max(rms)
    threshold = max_rms * 0.1  # 10% of max

    onset_frame = np.argmax(rms > threshold)
    peak_frame = np.argmax(rms)

    # Convert frames to time
    hop_length = int(0.01 * sr)
    attack_time = (peak_frame - onset_frame) * hop_length / sr

    return attack_time


def calc_auto_correlation(audio):
    """
    Calculates the autocorrelation of audio
    Basically you change the phase(shift the time) to find the sweet spot 
    """
    autocorr = librosa.autocorrelate(audio)

    return autocorr.tolist()


def calc_spectral_bandwidth(audio, sr):
    """
     Spectral bandwidth, spreads around center frequencies
     If not, wide harmonics and complex sound
    """
    bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
    mean_bandwidth = np.mean(bandwidth)

    return mean_bandwidth


# needs to be fixed
# i dont want mean but the array for visualisation
def calc_spectral_flux(audio, sr):
    """
    Measures how quickly the spectrum changes one frame to another
    """
    D = librosa.stft(y=audio,hop_length=config.HOP_LENGTH)
    # magnitude, phase = librosa.magphase(D) # get this way when you also want phase
    magnitude = np.abs(D)  # Fast, simple
    # difference between consecutive time frames
    diff = np.diff(magnitude, axis=1)

    # square all diff
    squared_diff = np.square(diff)

    # sum across all square bins
    sum_per_frame = np.sum(squared_diff, axis=0)

    flux = np.sqrt(sum_per_frame)

    return flux.tolist()


def calc_spectral_contrast(audio, sr):
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr, n_bands=6)

    return np.mean(spectral_contrast, axis=1).tolist()


def calc_mel_spec(audio, sr) -> tuple[float, float]:
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_mean = np.mean(mel_spec_db, axis=1).tolist()
    mel_spec_std = np.std(mel_spec_db, axis=1).tolist()

    return mel_spec_mean, mel_spec_std


def calc_chromagram(audio, sr):
    """
    Chromagram is energy distribution across 12 notes  
    """

    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

    return np.mean(chroma, axis=1).tolist()


def calc_tonnetz(audio, sr):
    """
    Tonnetz = Tonal Centroid Feature
    6-dimensional representation of harmonic content of given audio
    
    Dimensions:
    Major third relationships (C-E, F-A)
    Minor third relationships (C-Eb, E-G)
    Perfect fifth relationships (C-G, D-A)
    
    Each dimension has 2 axes(positive-negative)
    
    We can observe harmonic stability 
    """
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)

    return np.mean(tonnetz, axis=1).tolist()


def calc_rhythm_specs(audio, sr) -> tuple[float, float, float, float]:
    """
    Extract all rhythm specs
    Tempo, Tempo Confidence
    Onset density : Number of attacks per second
    Beat Strength : how strong are the beats
    """
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Calculate confidence from beat regularity
    if len(beat_frames) > 1:
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_intervals = np.diff(beat_times)
        interval_cv = np.std(beat_intervals) / (np.mean(beat_intervals) + 1e-10)
        tempo_confidence = np.exp(-interval_cv * 5)
        tempo_confidence = np.clip(tempo_confidence, 0, 1)
    else:
        tempo_confidence = 0.0

    if len(beat_frames) > 0:
        beat_strengths = onset_env[beat_frames]
        avg_beat_strength = np.mean(beat_strengths)
        overall_strength = np.mean(onset_env)
        beat_strength = avg_beat_strength / (overall_strength + 1e-10)
    else:
        beat_strength = 0.0

    onset_frames = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    duration = librosa.get_duration(y=audio, sr=sr)
    onset_density = len(onset_times) / duration if duration > 0 else 0.0

    return safe_float(tempo[0]), tempo_confidence, beat_strength, onset_density


def calc_rms_mean(audio):
    rms = librosa.feature.rms(y=audio)[0]
    rms_mean = np.mean(rms)

    return safe_float(rms_mean)


def calc_spectral_centroid(audio, sr):
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]

    return safe_float(np.mean(spectral_centroid))


def calc_silence_ratio(audio):
    """
    we assume that silence ratio something like 5 percent of max rms 
    """
    rms = librosa.feature.rms(y=audio)[0]
    max_rms = np.max(rms)
    threshold = max_rms * 0.05
    silence_ratio = np.sum(rms < threshold) / len(rms)

    return safe_float(silence_ratio)


def calc_max_amplitude(audio):
    max_amplitude = np.max(audio)

    return safe_float(max_amplitude)


def calc_snr(audio):
    """
    we assume that noise ratio is something like 10 percent of max rms  
    """
    rms = librosa.feature.rms(y=audio)[0]
    # noise threshold
    noise_threshold = np.percentile(rms, 10)
    noise_frames = rms[rms <= noise_threshold]
    noise_power = np.mean(noise_frames ** 2)
    # signal threshold
    signal_frames = rms[rms > noise_threshold]
    signal_power = np.mean(signal_frames ** 2)
    # null check
    if len(noise_frames) == 0 or len(signal_frames) == 0:
        return np.nan

    sound_to_noise_ratio = 10 * np.log10(signal_power / noise_power)

    return safe_float(sound_to_noise_ratio)


def calc_dynamic_range(audio):
    max_amplitude = np.max(audio)
    # watch out for complete silence
    min_amplitude = np.percentile(np.abs(audio), 1)
    dynamic_range_db = 10 * np.log10(np.abs(max_amplitude / min_amplitude))

    return safe_float(dynamic_range_db)


def calc_signal_to_quantization_noise_ratio(audio):
    # max signal strength / quantization error ratio
    signal_rms = np.sqrt(np.mean(audio ** 2))

    # this is the main formula for SQNR
    # 6.02~ is 20xlog10(2) , each additional bit doubles the quantization level(2**N), approx. 6dB
    # 1.76 and np.sqrt(12) are statistical properties
    # quantization_step = 1 / ((6.02 * 16 * 1.76) / 2)
    # quantization_noise_rms = quantization_step / np.sqrt(12) 
    # 32768 is standard and half of the 65536, which is 2^16, CDs are 16 bits
    quantization_step = 1.0 / 32768
    quantization_noise_rms = quantization_step / np.sqrt(12)

    sqnr_db = 10 * np.log10((signal_rms / quantization_noise_rms) ** 2)

    return safe_float(sqnr_db)


def calc_bandwidth(audio) -> tuple[float, float]:
    bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=16000)
    bandwidth_mean = np.mean(bandwidth)
    bandwidth_std = np.std(bandwidth)

    return safe_float(bandwidth_mean), safe_float(bandwidth_std)


def calc_band_energy_ratio(audio, sr):
    """
    we will use low/high as band energy ratio 
    """
    D = librosa.stft(audio)
    magnitude = np.abs(D) ** 2
    # frequency bins - lows- mids - highs
    frequencies = librosa.fft_frequencies(sr=sr)
    low_band_mask = frequencies <= 2000
    high_band_mask = frequencies > 2000
    # calc energies given dimensions
    low_band_energy = np.sum(magnitude[low_band_mask, :])
    high_band_energy = np.sum(magnitude[high_band_mask, :])
    # just to be sure
    if high_band_energy == 0:
        return 0
    band_energy_ratio = low_band_energy / high_band_energy
    band_energy_ratio_db = 10 * np.log10(band_energy_ratio)

    return safe_float(band_energy_ratio_db)


def calc_spectral_rolloff(audio, sr):
    """
    where total energy resides in an audio 
    """
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr, roll_percent=0.85)
    rolloff_mean = np.mean(rolloff)

    return safe_float(rolloff_mean)


def calc_spectral_flatness(audio):
    """
    returns how frequencies is distributed
    0 is tonal, 1 is noise-like
    """
    flatness = librosa.feature.spectral_flatness(y=audio)[0]
    flatness_mean = np.mean(flatness)

    return safe_float(flatness_mean)


def calc_mfcc(audio, sr) -> tuple[[float], float, float]:
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mfcc_variance = np.var(mfccs, axis=1).tolist()
    mfcc_mean = np.mean(mfccs, axis=1).tolist()

    return mfccs.tolist(), mfcc_mean, mfcc_variance


def calc_mfcc_variance(audio, sr):
    """
    returns how much variance is distributed
    detects variability in an audio, in terms of characteristics 
    """
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mfcc_variance = np.mean(np.var(mfccs, axis=1))

    return safe_float(mfcc_variance)


# helper to handle edge cases Infinity or Nan
def safe_float(value) -> float | None:
    if value is None:
        return None
    if np.isinf(value) or np.isnan(value):
        return None
    return float(value)