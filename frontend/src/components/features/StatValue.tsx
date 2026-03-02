interface Props {
  label: string
  value: number | null
  unit?: string
  decimals?: number
}

export default function StatValue({ label, value, unit = '', decimals = 3 }: Props) {
  return (
    <div className="flex items-center justify-between px-3 py-2 rounded-lg bg-zinc-900 border border-zinc-800 animate-fade-in">
      <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
      <span className="text-sm font-mono text-zinc-100">
        {value !== null ? `${value.toFixed(decimals)}${unit}` : '—'}
      </span>
    </div>
  )
}
