import { useState } from 'react'
import { Send } from 'lucide-react'

interface Props {
  categories: string[]
  onSubmit: (answer: string) => void
  loading: boolean
}

export default function GuessInput({ categories, onSubmit, loading }: Props) {
  const [selected, setSelected] = useState('')

  const handleSubmit = () => {
    if (!selected) return
    onSubmit(selected)
  }

  return (
    <div className="flex gap-2">
      <select
        value={selected}
        onChange={e => setSelected(e.target.value)}
        className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2.5 text-sm font-mono text-zinc-200
          focus:outline-none focus:border-indigo-500 transition-colors appearance-none cursor-pointer"
      >
        <option value="" disabled>Select sound type...</option>
        {categories.map(c => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
      <button
        onClick={handleSubmit}
        disabled={!selected || loading}
        className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500
          disabled:opacity-40 disabled:cursor-not-allowed text-sm font-semibold transition-colors"
      >
        <Send size={14} />
        <span>Guess</span>
      </button>
    </div>
  )
}
