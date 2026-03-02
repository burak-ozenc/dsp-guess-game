import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, Volume2, RotateCcw, Trophy } from 'lucide-react'
import { useGameStore } from '../store/gameStore'

export default function Reveal() {
  const navigate = useNavigate()
  const audioRef = useRef<HTMLAudioElement>(null)
  const { reveal, result, difficulty, reset } = useGameStore()

  useEffect(() => {
    if (!reveal) navigate('/')
  }, [])

  if (!reveal || !result) return null

  const handlePlayAgain = () => {
    reset()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-bg flex flex-col items-center justify-center gap-8 p-6 animate-fade-in">
      {/* Result */}
      <div className={`flex flex-col items-center gap-3 p-8 rounded-2xl border w-full max-w-md text-center
        ${result.correct
          ? 'border-emerald-500/30 bg-emerald-500/5'
          : 'border-red-500/30 bg-red-500/5'
        }`}
      >
        {result.correct
          ? <CheckCircle size={40} className="text-emerald-400" />
          : <XCircle size={40} className="text-red-400" />
        }
        <div>
          <p className="text-zinc-400 text-sm">The sound was</p>
          <p className="text-2xl font-bold font-mono mt-1">{reveal.category}</p>
          {reveal.subcategory && (
            <p className="text-sm text-zinc-500 mt-0.5">{reveal.subcategory}</p>
          )}
        </div>
        {!result.correct && (
          <p className="text-sm text-red-400">You guessed: <span className="font-mono">{result.correct_answer}</span></p>
        )}
      </div>

      {/* Score breakdown */}
      <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex flex-col gap-2">
        <div className="flex items-center gap-2 mb-1">
          <Trophy size={14} className="text-amber-400" />
          <span className="text-sm font-semibold">Round Summary</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-zinc-400 font-mono">Difficulty</span>
          <span className="font-mono capitalize">{difficulty}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-zinc-400 font-mono">Hints used</span>
          <span className="font-mono">{reveal.hints_used}</span>
        </div>
        <div className="flex justify-between text-sm border-t border-zinc-800 pt-2 mt-1">
          <span className="text-zinc-400 font-mono">Score</span>
          <span className={`font-mono font-bold text-base ${result.correct ? 'text-emerald-400' : 'text-zinc-600'}`}>
            {result.correct ? `+${result.score}` : '0'}
          </span>
        </div>
      </div>

      {/* Audio player */}
      {reveal.audio_url && (
        <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <Volume2 size={14} className="text-indigo-400" />
            <span className="text-sm font-semibold">Listen to the sample</span>
          </div>
          <audio
            ref={audioRef}
            controls
            src={reveal.audio_url}
            className="w-full h-8 accent-indigo-500"
          />
          <p className="text-[11px] text-zinc-600 font-mono">Audio link expires in 5 minutes</p>
        </div>
      )}

      <button
        onClick={handlePlayAgain}
        className="flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500
          font-semibold text-sm tracking-wide transition-colors"
      >
        <RotateCcw size={14} />
        Play Again
      </button>
    </div>
  )
}
