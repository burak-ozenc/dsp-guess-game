import {useMemo} from 'react'

interface Props {
    label: string
    data: number[]
    color?: string
    height?: number
}

export default function LineChart({label, data, color = '#6366f1', height = 48}: Props) {
    const path = useMemo(() => {
        if (!data.length) return ''
        const w = 300
        const h = height
        const min = data.reduce((a, b) => Math.min(a, b), Infinity)
        const max = data.reduce((a, b) => Math.max(a, b), -Infinity)
        const range = max - min || 1
        const step = w / (data.length - 1)

        return data
            .map((v, i) => {
                const x = i * step
                const y = h - ((v - min) / range) * h
                return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`
            })
            .join(' ')
    }, [data, height])

    const areaPath = `${path} L 300 ${height} L 0 ${height} Z`

    return (
        <div className="flex flex-col gap-1.5 animate-fade-in">
            <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
            <div className="rounded-lg bg-zinc-900 border border-zinc-800 overflow-hidden p-2">
                <svg viewBox={`0 0 300 ${height}`} className="w-full" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id={`grad-${label}`} x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor={color} stopOpacity="0.3"/>
                            <stop offset="100%" stopColor={color} stopOpacity="0.02"/>
                        </linearGradient>
                    </defs>
                    <path d={areaPath} fill={`url(#grad-${label})`}/>
                    <path d={path} fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round"
                          strokeLinejoin="round"/>
                </svg>
            </div>
            <div className="flex justify-between">
                <span className="text-[10px] text-zinc-600 font-mono">0</span>
                <span className="text-[10px] text-zinc-600 font-mono">{data.length} frames</span>
            </div>
        </div>
    )
}
