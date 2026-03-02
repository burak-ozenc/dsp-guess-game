import { useMemo } from 'react'

interface Props {
  label: string
  data: number[]
  axisLabels?: string[]
  color?: string
}

export default function RadarChart({ label, data, axisLabels, color = '#6366f1' }: Props) {
  const size = 120
  const cx = size / 2
  const cy = size / 2
  const r = size * 0.38

  const max = Math.max(...data.map(Math.abs)) || 1

  const points = useMemo(() => {
    return data.map((v, i) => {
      const angle = (i / data.length) * Math.PI * 2 - Math.PI / 2
      const mag = (v / max) * r
      return {
        x: cx + mag * Math.cos(angle),
        y: cy + mag * Math.sin(angle),
        lx: cx + (r + 14) * Math.cos(angle),
        ly: cy + (r + 14) * Math.sin(angle),
      }
    })
  }, [data, max, r, cx, cy])

  const polyPoints = points.map(p => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')

  const gridLevels = [0.33, 0.66, 1]

  return (
    <div className="flex flex-col gap-1.5 animate-fade-in">
      <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
      <div className="rounded-lg bg-zinc-900 border border-zinc-800 p-2 flex justify-center">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
          {/* grid rings */}
          {gridLevels.map((lvl, gi) => {
            const gpts = data.map((_, i) => {
              const angle = (i / data.length) * Math.PI * 2 - Math.PI / 2
              return `${(cx + r * lvl * Math.cos(angle)).toFixed(1)},${(cy + r * lvl * Math.sin(angle)).toFixed(1)}`
            }).join(' ')
            return <polygon key={gi} points={gpts} fill="none" stroke="#1e1e2e" strokeWidth="1" />
          })}
          {/* spokes */}
          {points.map((p, i) => (
            <line key={i} x1={cx} y1={cy} x2={(cx + r * Math.cos((i / data.length) * Math.PI * 2 - Math.PI / 2)).toFixed(1)} y2={(cy + r * Math.sin((i / data.length) * Math.PI * 2 - Math.PI / 2)).toFixed(1)} stroke="#1e1e2e" strokeWidth="1" />
          ))}
          {/* fill */}
          <polygon points={polyPoints} fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1.5" strokeLinejoin="round" />
          {/* dots */}
          {points.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r="2" fill={color} />
          ))}
          {/* labels */}
          {axisLabels && points.map((p, i) => (
            <text key={i} x={p.lx} y={p.ly} textAnchor="middle" dominantBaseline="middle" fontSize="7" fill="#71717a" fontFamily="JetBrains Mono">
              {axisLabels[i]}
            </text>
          ))}
        </svg>
      </div>
    </div>
  )
}
