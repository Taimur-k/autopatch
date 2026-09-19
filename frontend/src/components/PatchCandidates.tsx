import { useState } from 'react'
import type { PatchCandidate } from '../types'
import DiffViewer from './DiffViewer'

interface Props {
  patches: PatchCandidate[]
}

const TEST_STATUS_STYLE: Record<string, string> = {
  PASSED:  'text-green-400',
  FAILED:  'text-red-400',
  ERROR:   'text-orange-400',
  PENDING: 'text-gray-500',
}

export default function PatchCandidates({ patches }: Props) {
  const [expanded, setExpanded] = useState<string | null>(null)

  if (patches.length === 0) {
    return <p className="text-sm text-gray-500">No patches generated yet.</p>
  }

  return (
    <div className="space-y-3">
      {patches.map((patch, idx) => (
        <div key={patch.id} className="border border-gray-800 rounded-lg overflow-hidden">
          {/* Header row */}
          <button
            onClick={() => setExpanded(expanded === patch.id ? null : patch.id)}
            className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-800/60 transition-colors text-left"
          >
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-gray-500">#{idx + 1}</span>
              <span className="text-sm text-gray-200">{patch.description}</span>
            </div>
            <div className="flex items-center gap-4 shrink-0">
              <span className={`text-xs font-mono font-semibold ${TEST_STATUS_STYLE[patch.test_status]}`}>
                {patch.test_status}
              </span>
              <span className="text-xs text-gray-500">
                score <span className="text-white font-mono">{patch.final_score.toFixed(2)}</span>
              </span>
              <span className="text-gray-600 text-xs">{expanded === patch.id ? '▲' : '▼'}</span>
            </div>
          </button>

          {/* Expanded diff */}
          {expanded === patch.id && (
            <div className="border-t border-gray-800">
              <DiffViewer diff={patch.diff} />
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

