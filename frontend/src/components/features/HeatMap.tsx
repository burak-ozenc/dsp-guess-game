import {useMemo} from 'react'

interface Props {
    label: string
    data: number[][]  // [n_coeffs][n_frames]
}

export default function HeatMap({label, data}: Props) {
    const {min, max} = useMemo(() => {
        const flat = data.flat()
        return {
            min: flat.reduce((a, b) => Math.min(a, b), Infinity),
            max: flat.reduce((a, b) => Math.max(a, b), -Infinity),
        }
    }, [data])

    const range = max - min || 1

    // Sample frames to keep render fast — max 60 columns
    const sampled = useMemo(() => {
        const nFrames = data[0]?.length ?? 0
        const step = Math.max(1, Math.floor(nFrames / 60))
        return data.map(row => row.filter((_, i) => i % step === 0))
    }, [data])

    const nCoeffs = sampled.length
    const nFrames = sampled[0]?.length ?? 0

    return (
        <div className="flex flex-col gap-1.5 animate-fade-in">
            <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider">{label}</span>
            <div className="rounded-lg bg-zinc-900 border border-zinc-800 p-2 overflow-hidden">
                <div
                    className="grid gap-px"
                    style={{
                        gridTemplateRows: `repeat(${nCoeffs}, 1fr)`,
                        gridTemplateColumns: `repeat(${nFrames}, 1fr)`
                    }}
                >
                    {sampled.map((row, ci) =>
                        row.map((v, fi) => {
                            const pct = (v - min) / range
                            const r = Math.round(99 + pct * (165 - 99))
                            const g = Math.round(102 + pct * (80 - 102))
                            const b = Math.round(241 + pct * (162 - 241))
                            return (
                                <div
                                    key={`${ci}-${fi}`}
                                    style={{
                                        backgroundColor: `rgb(${r},${g},${b})`,
                                        height: 6,
                                        opacity: 0.8 + pct * 0.2
                                    }}
                                />
                            )
                        })
                    )}
                </div>
                <div className="flex justify-between mt-1">
                    <span className="text-[10px] text-zinc-600 font-mono">coeff 0</span>
                    <span className="text-[10px] text-zinc-600 font-mono">coeff {nCoeffs - 1}</span>
                </div>
            </div>
        </div>
    )
}
