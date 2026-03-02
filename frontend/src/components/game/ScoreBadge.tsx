import { Trophy } from 'lucide-react'

interface Props {
  score: number
  correct: boolean
}

export default function ScoreBadge({ score, correct }: Props) {
  return (
    <div className={`flex items-center gap-2 px-4 py-2 rounded-lg border font-mono text-sm
      ${correct
        ? 'border-emerald-600/50 bg-emerald-500/10 text-emerald-400'
        : 'border-red-600/50 bg-red-500/10 text-red-400'
      }`}
    >
      <Trophy size={14} />
      <span>{correct ? 'Correct!' : 'Wrong'}</span>
      {correct && <span className="ml-1 font-bold">+{score}</span>}
    </div>
  )
}
