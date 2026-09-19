import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import RunStatus from '../components/RunStatus'
import type { RepairRun, RepairStatus, RepairStage } from '../types'

// Mock runs shown until the API is fully wired up.
const MOCK_RUNS: (RepairRun & { repo: string; issue: string })[] = [
  {
    id: 'run-001',
    issue_id: 'issue-001',
    status: 'COMPLETED',
    current_stage: 'COMPLETED',
    started_at: new Date(Date.now() - 3 * 60 * 1000).toISOString(),
    completed_at: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
    repo: 'acme-corp/billing-service',
    issue: 'IndexError when parsing empty input',
  },
  {
    id: 'run-002',
    issue_id: 'issue-002',
    status: 'RUNNING',
    current_stage: 'GENERATING_PATCH',
    started_at: new Date(Date.now() - 45 * 1000).toISOString(),
    completed_at: null,
    repo: 'acme-corp/auth-service',
    issue: 'NullPointerException on login with empty password',
  },
  {
    id: 'run-003',
    issue_id: 'issue-003',
    status: 'FAILED',
    current_stage: 'VALIDATING_PATCH',
    started_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
    completed_at: new Date(Date.now() - 8 * 60 * 1000).toISOString(),
    repo: 'acme-corp/data-pipeline',
    issue: 'KeyError in ETL transform step',
  },
]

function formatDuration(start: string, end: string | null): string {
  const startMs = new Date(start).getTime()
  const endMs = end ? new Date(end).getTime() : Date.now()
  const secs = Math.round((endMs - startMs) / 1000)
  if (secs < 60) return `${secs}s`
  return `${Math.floor(secs / 60)}m ${secs % 60}s`
}

export default function Dashboard() {
  const [runs] = useState(MOCK_RUNS)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Repair Runs</h1>
          <p className="text-sm text-gray-500 mt-1">Recent automated program repair sessions.</p>
        </div>
        <Link
          to="/new"
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-lg transition-colors"
        >
          + New Repair
        </Link>
      </div>

      {/* Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-xs text-gray-500">
              <th className="text-left px-5 py-3 font-medium">Repository</th>
              <th className="text-left px-5 py-3 font-medium">Issue</th>
              <th className="text-left px-5 py-3 font-medium">Status</th>
              <th className="text-left px-5 py-3 font-medium">Stage</th>
              <th className="text-left px-5 py-3 font-medium">Duration</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {runs.map(run => (
              <tr
                key={run.id}
                className="hover:bg-gray-800/50 transition-colors cursor-pointer"
                onClick={() => window.location.href = `/runs/${run.id}`}
              >
                <td className="px-5 py-3 font-mono text-blue-400 text-xs">{run.repo}</td>
                <td className="px-5 py-3 text-gray-300 max-w-xs truncate">{run.issue}</td>
                <td className="px-5 py-3">
                  <RunStatus status={run.status} />
                </td>
                <td className="px-5 py-3 font-mono text-xs text-gray-500">{run.current_stage}</td>
                <td className="px-5 py-3 font-mono text-xs text-gray-500">
                  {formatDuration(run.started_at, run.completed_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {runs.length === 0 && (
          <div className="text-center py-16 text-gray-600">
            <p className="text-4xl mb-3">🩹</p>
            <p className="font-medium">No repair runs yet.</p>
            <p className="text-sm mt-1">Start your first repair to see it here.</p>
          </div>
        )}
      </div>
    </div>
  )
}

