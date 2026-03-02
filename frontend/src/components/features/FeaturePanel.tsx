import { useState } from 'react'
import { ChevronDown } from 'lucide-react'

interface Props {
  title: string
  icon: React.ReactNode
  children: React.ReactNode
  defaultOpen?: boolean
}

export default function FeaturePanel({ title, icon, children, defaultOpen = true }: Props) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="rounded-xl border border-zinc-800 overflow-hidden animate-slide-up">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-zinc-900 hover:bg-zinc-800/80 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="text-indigo-400">{icon}</span>
          <span className="text-sm font-semibold tracking-wide">{title}</span>
        </div>
        <ChevronDown
          size={14}
          className={`text-zinc-500 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
        />
      </button>
      {open && (
        <div className="px-4 py-3 bg-zinc-950 flex flex-col gap-3">
          {children}
        </div>
      )}
    </div>
  )
}
