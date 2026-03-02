import {useEffect} from 'react'
import {useNavigate} from 'react-router-dom'
import { CheckCircle, XCircle, Volume2, RotateCcw, Clock, Radio, Mic, Signal } from 'lucide-react'
import {useGameStore} from '../store/gameStore'
import FeaturePanel from '../components/features/FeaturePanel'
import LineChart from '../components/features/LineChart'
import Gauge from '../components/features/Gauge'
import BarChart from '../components/features/BarChart'
import HeatMap from '../components/features/HeatMap'
import RadarChart from '../components/features/RadarChart'
import StatValue from '../components/features/StatValue'
import LockedFeature from '../components/ui/LockedFeature'
import HintButton from '../components/game/HintButton'
import GuessInput from '../components/game/GuessInput'
import ScoreBadge from '../components/game/ScoreBadge'

const CHROMA_LABELS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
const TONNETZ_LABELS = ['5th+', '5th-', 'min3+', 'min3-', 'maj3+', 'maj3-']
const CONTRAST_LABELS = ['Sub', 'Low', 'Mid-L', 'Mid', 'Mid-H', 'High', 'Bri']

export default function Game() {
    const navigate = useNavigate()
    const {
        features, difficulty, hintsRemaining, categories,
        result, loading, error,
        useHint, submitGuess, reveal, fetchCategories, reset,
    } = useGameStore()

    useEffect(() => {
        if (!features) {
            navigate('/');
            return
        }
        if (categories.length === 0) fetchCategories()
    }, [])

    if (!features) return null
    
    const td = features.time_domain
    const sp = features.spectral
    const pc = features.perceptual
    const rh = features.rhythm
    const qu = features.quality

    const diffLabel = difficulty ? difficulty.charAt(0).toUpperCase() + difficulty.slice(1) : ''

    return (
        <div className="min-h-screen bg-bg">
            {/* Top bar */}
            <div className="sticky top-0 z-10 bg-bg/95 backdrop-blur border-b border-zinc-800 px-4 py-3">
                <div className="max-w-2xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <span className="text-sm font-mono font-bold text-white">Signal<span
                            className="text-indigo-400">.</span>Guess</span>
                        <span
                            className="text-xs font-mono px-2 py-0.5 rounded-full border border-zinc-700 text-zinc-400">{diffLabel}</span>
                    </div>
                    <HintButton hintsRemaining={hintsRemaining} onUseHint={useHint} loading={loading}/>
                </div>
            </div>

            <div className="max-w-2xl mx-auto px-4 py-6 flex flex-col gap-4">

                {/* ── Time Domain ─────────────────────────────── */}
                <FeaturePanel title="Time Domain" icon={<Clock size={14}/>}>
                    {td.rms_energy ? <LineChart label="RMS Energy" data={td.rms_energy}/> :
                        <LockedFeature label="rms_energy"/>}
                    {td.zcr ? <LineChart label="ZCR" data={td.zcr} color="#8b5cf6"/> : <LockedFeature label="zcr"/>}
                    {td.crest_factor != null
                        ? <Gauge label="Crest Factor (dB)" value={td.crest_factor} min={0} max={40} unit=" dB"/>
                        : <LockedFeature label="crest_factor"/>}
                    {td.attack_time_ms != null
                        ? <StatValue label="Attack Time" value={td.attack_time_ms} unit=" ms" decimals={1}/>
                        : <LockedFeature label="attack_time_ms"/>}
                    {td.autocorr ? <LineChart label="Autocorrelation" data={td.autocorr} color="#a78bfa"/> :
                        <LockedFeature label="autocorr"/>}
                </FeaturePanel>

                {/* ── Frequency Domain ────────────────────────── */}
                <FeaturePanel title="Frequency Domain" icon={<Radio size={14}/>}>
                    {sp.spectral_centroid != null
                        ?
                        <Gauge label="Spectral Centroid (Hz)" value={sp.spectral_centroid} min={0} max={8000} unit=" Hz"
                               decimals={0}/>
                        : <LockedFeature label="spectral_centroid"/>}
                    {sp.spectral_bandwidth != null
                        ? <Gauge label="Spectral Bandwidth (Hz)" value={sp.spectral_bandwidth} min={0} max={8000}
                                 unit=" Hz" decimals={0}/>
                        : <LockedFeature label="spectral_bandwidth"/>}
                    {sp.spectral_rolloff != null
                        ? <Gauge label="Spectral Rolloff (Hz)" value={sp.spectral_rolloff} min={0} max={8000} unit=" Hz"
                                 decimals={0}/>
                        : <LockedFeature label="spectral_rolloff"/>}
                    {sp.spectral_flatness != null
                        ? <Gauge label="Spectral Flatness" value={sp.spectral_flatness} min={0} max={1}/>
                        : <LockedFeature label="spectral_flatness"/>}
                    {sp.spectral_flux ? <LineChart label="Spectral Flux" data={sp.spectral_flux} color="#ec4899"/> :
                        <LockedFeature label="spectral_flux"/>}
                    {sp.spectral_contrast
                        ? <BarChart label="Spectral Contrast (dB)" data={sp.spectral_contrast}
                                    barLabels={CONTRAST_LABELS}/>
                        : <LockedFeature label="spectral_contrast"/>}
                </FeaturePanel>

                {/* ── Perceptual / Timbral ────────────────────── */}
                <FeaturePanel title="Perceptual / Timbral" icon={<Mic size={14}/>}>
                    {pc.mfcc_mean
                        ? <BarChart label="MFCC Mean (per coeff)" data={pc.mfcc_mean}
                                    barLabels={pc.mfcc_mean.map((_, i) => `${i}`)}/>
                        : <LockedFeature label="mfcc_mean"/>}
                    {pc.mfcc_variance
                        ? <BarChart label="MFCC Variance (per coeff)" data={pc.mfcc_variance}
                                    barLabels={pc.mfcc_variance.map((_, i) => `${i}`)} color="#a78bfa"/>
                        : <LockedFeature label="mfcc_variance"/>}
                    {pc.mfcc ? <HeatMap label="MFCC Heatmap" data={pc.mfcc}/> : <LockedFeature label="mfcc"/>}
                    {pc.mel_stats_mean
                        ? <BarChart label="Mel Stats Mean" data={pc.mel_stats_mean} color="#06b6d4"/>
                        : <LockedFeature label="mel_stats_mean"/>}
                    {pc.chroma
                        ? <RadarChart label="Chroma (12 pitch classes)" data={pc.chroma} axisLabels={CHROMA_LABELS}/>
                        : <LockedFeature label="chroma"/>}
                    {pc.tonnetz
                        ? <RadarChart label="Tonnetz (6 tonal dims)" data={pc.tonnetz} axisLabels={TONNETZ_LABELS}
                                      color="#f59e0b"/>
                        : <LockedFeature label="tonnetz"/>}
                </FeaturePanel>

                {/* ── Rhythm ──────────────────────────────────── */}
                <FeaturePanel title="Rhythm / Temporal" icon={<Mic size={14}/>}>
                    {rh.onset_density != null
                        ? <StatValue label="Onset Density" value={rh.onset_density} unit=" /s" decimals={2}/>
                        : <LockedFeature label="onset_density"/>}
                    {rh.tempo_bpm != null
                        ? <StatValue label="Tempo" value={rh.tempo_bpm} unit=" BPM" decimals={1}/>
                        : <LockedFeature label="tempo_bpm"/>}
                    {rh.tempo_confidence != null
                        ? <Gauge label="Tempo Confidence" value={rh.tempo_confidence} min={0} max={1}/>
                        : <LockedFeature label="tempo_confidence"/>}
                    {rh.beat_strength != null
                        ? <StatValue label="Beat Strength" value={rh.beat_strength} decimals={3}/>
                        : <LockedFeature label="beat_strength"/>}
                </FeaturePanel>

                {/* ── Signal Quality ──────────────────────────── */}
                <FeaturePanel title="Signal Quality" icon={<Signal size={14}/>}>
                    {qu.snr_db != null
                        ? <Gauge label="SNR" value={qu.snr_db} min={-10} max={60} unit=" dB"/>
                        : <LockedFeature label="snr_db"/>}
                    {qu.dynamic_range_db != null
                        ? <Gauge label="Dynamic Range" value={qu.dynamic_range_db} min={0} max={60} unit=" dB"/>
                        : <LockedFeature label="dynamic_range_db"/>}
                    {qu.silence_ratio != null
                        ? <Gauge label="Silence Ratio" value={qu.silence_ratio} min={0} max={1}/>
                        : <LockedFeature label="silence_ratio"/>}
                    {qu.clipping_ratio != null
                        ? <Gauge label="Clipping Ratio" value={qu.clipping_ratio} min={0} max={1}/>
                        : <LockedFeature label="clipping_ratio"/>}
                    {qu.thd_percent != null
                        ? <StatValue label="THD" value={qu.thd_percent} unit="%" decimals={3}/>
                        : <LockedFeature label="thd_percent"/>}
                </FeaturePanel>

                {/* ── Guess Area ──────────────────────────────── */}
                <div className="sticky bottom-4 mt-2">
                    <div className="bg-zinc-900/95 backdrop-blur border border-zinc-700 rounded-2xl p-4 flex flex-col gap-3 shadow-2xl">
                        {error && <p className="text-red-400 text-xs font-mono">{error}</p>}

                        {!result && (
                            <GuessInput categories={categories} onSubmit={submitGuess} loading={loading} />
                        )}

                        {result && reveal && (
                            <>
                                {/* Result */}
                                <div className={`flex items-center gap-3 px-3 py-2 rounded-lg border text-sm font-mono
          ${result.correct
                                    ? 'border-emerald-600/50 bg-emerald-500/10 text-emerald-400'
                                    : 'border-red-600/50 bg-red-500/10 text-red-400'
                                }`}
                                >
                                    {result.correct ? <CheckCircle size={14} /> : <XCircle size={14} />}
                                    <span>{result.correct ? 'Correct!' : `Wrong — it was `}</span>
                                    {!result.correct && <span className="font-bold">{result.correct_answer}</span>}
                                </div>

                                {/* Audio player */}
                                {reveal.audio_url && (
                                    <div className="flex flex-col gap-1.5">
                                        <div className="flex items-center gap-2">
                                            <Volume2 size={12} className="text-indigo-400" />
                                            <span className="text-xs text-zinc-400">Listen to the sample</span>
                                        </div>
                                        <audio controls src={reveal.audio_url} className="w-full h-8 accent-indigo-500" />
                                    </div>
                                )}

                                {/* Play again */}
                                <button
                                    onClick={() => { reset(); navigate('/') }}
                                    className="flex items-center justify-center gap-2 py-2 rounded-lg border border-zinc-700
            hover:border-zinc-500 text-sm text-zinc-300 transition-colors"
                                >
                                    <RotateCcw size={13} />
                                    Play Again
                                </button>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
