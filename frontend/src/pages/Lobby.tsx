import {useEffect, useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { useGameStore } from '../store/gameStore'
import type { Difficulty } from '../types/game'
import { Zap, Brain, Flame } from 'lucide-react'

const DIFFICULTIES: {
  value: Difficulty
  label: string
  description: string
  hints: string
  icon: React.ReactNode
  color: string
}[] = [
  {
    value: 'easy',
    label: 'Easy',
    description: 'Time domain + quality features visible',
    hints: 'No hints',
    icon: <Zap size={18} />,
    color: 'emerald',
  },
  {
    value: 'medium',
    label: 'Medium',
    description: 'Spectral features added, graphs locked',
    hints: '2 hints',
    icon: <Brain size={18} />,
    color: 'amber',
  },
  {
    value: 'hard',
    label: 'Hard',
    description: 'Start blind — unlock from complex to simple',
    hints: '5 hints',
    icon: <Flame size={18} />,
    color: 'red',
  },
]

const colorMap: Record<string, Record<string, string>> = {
  emerald: {
    border: 'border-emerald-500',
    bg: 'bg-emerald-500/10',
    icon: 'text-emerald-400',
    badge: 'bg-emerald-500/20 text-emerald-400',
  },
  amber: {
    border: 'border-amber-500',
    bg: 'bg-amber-500/10',
    icon: 'text-amber-400',
    badge: 'bg-amber-500/20 text-amber-400',
  },
  red: {
    border: 'border-red-500',
    bg: 'bg-red-500/10',
    icon: 'text-red-400',
    badge: 'bg-red-500/20 text-red-400',
  },
}

export default function Lobby() {
  const [selected, setSelected] = useState<Difficulty | null>(null)
  const { startSession, loading, error, fetchCategories } = useGameStore()
  const navigate = useNavigate()

  const handleStart = async () => {
    if (!selected) return
      console.log("Selected Difficulty",selected)
    await startSession(selected)
    navigate('/game')
  }

    useEffect(() => {
        fetchCategories()
    }, [])

  return (
    <div className="min-h-screen bg-bg flex flex-col items-center justify-center gap-10 p-6">
      {/* Header */}
      <div className="text-center animate-fade-in">
        <div className="inline-flex items-center gap-2 text-xs font-mono text-indigo-400 uppercase tracking-widest mb-3 border border-indigo-500/30 px-3 py-1 rounded-full">
          DSP Training
        </div>
        <h1 className="text-5xl font-bold tracking-tight font-mono text-white">
          Signal<span className="text-indigo-400">.</span>Guess
        </h1>
        <p className="text-zinc-400 mt-3 text-sm max-w-sm mx-auto leading-relaxed">
          Identify sounds from their signal characteristics. No audio — just numbers.
        </p>
      </div>

      {/* Difficulty Cards */}
      <div className="flex flex-col gap-3 w-full max-w-md animate-slide-up">
        {DIFFICULTIES.map(({ value, label, description, hints, icon, color }) => {
          const c = colorMap[color]
          const isSelected = selected === value
          return (
            <button
              key={value}
              onClick={() => setSelected(value)}
              className={`flex items-center gap-4 p-4 rounded-xl border transition-all text-left
                ${isSelected ? `${c.border} ${c.bg}` : 'border-zinc-800 hover:border-zinc-700 bg-zinc-900'}`}
            >
              <span className={`${isSelected ? c.icon : 'text-zinc-500'} transition-colors`}>{icon}</span>
              <div className="flex-1">
                <div className="font-semibold text-sm">{label}</div>
                <div className="text-xs text-zinc-400 mt-0.5">{description}</div>
              </div>
              <span className={`text-[11px] font-mono px-2 py-0.5 rounded-full ${isSelected ? c.badge : 'bg-zinc-800 text-zinc-500'}`}>
                {hints}
              </span>
            </button>
          )
        })}
      </div>

      {error && (
        <p className="text-red-400 text-sm font-mono border border-red-500/30 px-3 py-2 rounded-lg bg-red-500/10">
          {error}
        </p>
      )}

      <button
        onClick={handleStart}
        disabled={!selected || loading}
        className="w-full max-w-md py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500
          disabled:opacity-30 disabled:cursor-not-allowed font-semibold text-sm tracking-wide
          transition-all duration-200 animate-fade-in"
      >
        {loading ? 'Loading...' : 'Start Game →'}
      </button>
    </div>
  )
}
