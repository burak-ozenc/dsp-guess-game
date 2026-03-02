import { Lightbulb } from 'lucide-react'

interface Props {
  hintsRemaining: number
  onUseHint: () => void
  loading: boolean
}

export default function HintButton({ hintsRemaining, onUseHint, loading }: Props) {
  const disabled = hintsRemaining <= 0 || loading

  return (
    <button
      onClick={onUseHint}
      disabled={disabled}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg border text-sm font-medium transition-all
        ${disabled
          ? 'border-zinc-800 text-zinc-600 cursor-not-allowed'
          : 'border-amber-600/50 text-amber-400 hover:bg-amber-500/10 hover:border-amber-500'
        }`}
    >
      <Lightbulb size={14} />
      <span>Hint</span>
      {hintsRemaining > 0 && (
        <span className="ml-1 text-xs bg-amber-500/20 text-amber-400 rounded-full px-1.5 py-0.5">
          {hintsRemaining}
        </span>
      )}
    </button>
  )
}
