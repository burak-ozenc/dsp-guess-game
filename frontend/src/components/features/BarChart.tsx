import {useMemo} from 'react'

interface Props {
    label: string
    data: number[]
    barLabels?: string[]
    color?: string
}

export default function BarChart({label, data, barLabels, color = '#6366f1'}: Props) {
    const {min, max} = useMemo(() => ({
        min: data.reduce((a, b) => Math.min(a, b), Infinity),
        max: data.reduce((a, b) => Math.max(a, b), -Infinity),
    }), [data])
    const range = max - min || 1

    return (
        <div className="flex flex-col gap-1.5 animate-fade-in">
            <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
            <div className="rounded-lg bg-zinc-900 border border-zinc-800 p-3">
                <div className="flex items-end gap-px h-14">
                    {data.map((v, i) => {
                        const pct = (v - min) / range
                        const heightPx = Math.max(3, pct * 56)  // 56px = h-14
                        return (
                            <div key={i} className="flex-1 flex flex-col items-center justify-end" title={`${barLabels?.[i] ?? i}: ${v.toFixed(3)}`}>
                                <div
                                    className="w-full rounded-sm transition-all duration-700"
                                    style={{
                                        height: `${heightPx}px`,
                                        backgroundColor: color,
                                        opacity: 0.4 + pct * 0.6,
                                    }}
                                />
                            </div>
                        )
                    })}
                </div>
                {barLabels && (
                    <div className="flex gap-1 mt-1">
                        {barLabels.map((l, i) => (
                            <div key={i}
                                 className="flex-1 text-center text-[9px] text-zinc-600 font-mono truncate">{l}</div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
