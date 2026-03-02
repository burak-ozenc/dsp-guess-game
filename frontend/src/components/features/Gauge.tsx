interface Props {
  label: string
  value: number
  min?: number
  max?: number
  unit?: string
  decimals?: number
}

export default function Gauge({ label, value, min = 0, max = 1, unit = '', decimals = 2 }: Props) {
  const pct = Math.min(1, Math.max(0, (value - min) / (max - min)))
  const color = pct < 0.33 ? '#6366f1' : pct < 0.66 ? '#8b5cf6' : '#a78bfa'

  return (
    <div className="flex flex-col gap-1.5 animate-fade-in">
      <div className="flex justify-between items-center">
        <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
        <span className="text-xs font-mono text-zinc-200">
          {value.toFixed(decimals)}{unit}
        </span>
      </div>
      <div className="h-1.5 rounded-full bg-zinc-800 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700 ease-out"
          style={{ width: `${pct * 100}%`, backgroundColor: color }}
        />
      </div>
      <div className="flex justify-between">
        <span className="text-[10px] text-zinc-600 font-mono">{min}{unit}</span>
        <span className="text-[10px] text-zinc-600 font-mono">{max}{unit}</span>
      </div>
    </div>
  )
}
