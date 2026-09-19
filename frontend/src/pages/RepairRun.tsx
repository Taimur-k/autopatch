import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import RepairTimeline from '../components/RepairTimeline'
import FaultLocations from '../components/FaultLocations'
import PatchCandidates from '../components/PatchCandidates'
import TestResults, { MOCK_RESULTS } from '../components/TestResults'
import RunStatus from '../components/RunStatus'
import { getTimeline, getFaultLocations, getPatches, getRepairRun } from '../services/api'
import type { RepairRun, TimelineEvent, FaultLocation, PatchCandidate } from '../types'

// Placeholder run shown while data loads (or when backend is offline).
const PLACEHOLDER_RUN: RepairRun = {
  id: 'run-001',
  issue_id: 'issue-001',
  status: 'COMPLETED',
  current_stage: 'COMPLETED',
  started_at: new Date(Date.now() - 3 * 60 * 1000).toISOString(),
  completed_at: new Date().toISOString(),
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <div className="px-5 py-3 border-b border-gray-800">
        <h2 className="text-sm font-semibold text-gray-300">{title}</h2>
      </div>
      <div className="px-5 py-4">{children}</div>
    </div>
  )
}

export default function RepairRun() {
  const { runId } = useParams<{ runId: string }>()

  const [run, setRun] = useState<RepairRun>(PLACEHOLDER_RUN)
  const [timeline, setTimeline] = useState<TimelineEvent[]>([])
  const [faultLocations, setFaultLocations] = useState<FaultLocation[]>([])
  const [patches, setPatches] = useState<PatchCandidate[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!runId) return
    Promise.all([
      getRepairRun(runId),
      getTimeline(runId),
      getFaultLocations(runId),
      getPatches(runId),
    ])
      .then(([runData, tlData, flData, patchData]) => {
        setRun(runData)
        setTimeline(tlData)
        setFaultLocations(flData)
        setPatches(patchData)
      })
      .catch(() => {
        // Backend offline — keep placeholder data so UI remains useful.
      })
      .finally(() => setLoading(false))
  }, [runId])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="text-gray-500 hover:text-gray-300 text-sm transition-colors">
            ← All Runs
          </Link>
          <span className="text-gray-700">/</span>
          <span className="text-gray-400 font-mono text-sm">{runId}</span>
        </div>
        <RunStatus status={run.status} />
      </div>

      {loading && (
        <p className="text-sm text-gray-500 animate-pulse">Loading repair run data…</p>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Left column: pipeline timeline */}
        <div className="xl:col-span-1">
          <Section title="Pipeline">
            <RepairTimeline events={timeline} currentStage={run.current_stage} />
          </Section>
        </div>

        {/* Right columns: details */}
        <div className="xl:col-span-2 space-y-6">
          <Section title="Test Results">
            <TestResults results={MOCK_RESULTS} />
          </Section>

          <Section title="Fault Locations">
            <FaultLocations locations={faultLocations} />
          </Section>

          <Section title="Candidate Patches">
            <PatchCandidates patches={patches} />
          </Section>
        </div>
      </div>
    </div>
  )
}

