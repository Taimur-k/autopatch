import type { FaultLocation } from '../types'

interface Props {
  locations: FaultLocation[]
}

function ScoreBar({ score }: { score: number }) {
  const pct = Math.round(score * 100)
  const color =
    score >= 0.8 ? 'bg-red-500' :
    score >= 0.5 ? 'bg-yellow-500' :
    'bg-green-600'

  return (
    <div className="flex items-center gap-2">
      <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-mono text-gray-400">{score.toFixed(2)}</span>
    </div>
  )
}

export default function FaultLocations({ locations }: Props) {
  if (locations.length === 0) {
    return <p className="text-sm text-gray-500">No fault locations identified yet.</p>
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-xs text-gray-500 border-b border-gray-800">
          <th className="pb-2 font-medium">Location</th>
          <th className="pb-2 font-medium">Function</th>
          <th className="pb-2 font-medium">Suspiciousness</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-800">
        {locations.map((loc, i) => (
          <tr key={i} className="hover:bg-gray-800/50 transition-colors">
            <td className="py-2.5 pr-4 font-mono text-blue-400">
              {loc.file}
              <span className="text-gray-500">:{loc.line}</span>
            </td>
            <td className="py-2.5 pr-4 font-mono text-gray-400 text-xs">
              {loc.function ?? '—'}
            </td>
            <td className="py-2.5">
              <ScoreBar score={loc.suspiciousness_score} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

