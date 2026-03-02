import { Lock } from 'lucide-react'

interface Props {
  label: string
}

export default function LockedFeature({ label }: Props) {
  return (
    <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
      <Lock size={12} className="text-zinc-600 shrink-0" />
      <span className="text-xs text-zinc-600 font-mono">{label}</span>
      <div className="ml-auto flex gap-1">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="w-4 h-2 rounded-sm bg-zinc-800" />
        ))}
      </div>
    </div>
  )
}
