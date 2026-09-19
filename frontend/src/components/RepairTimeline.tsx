import type { TimelineEvent, RepairStage } from '../types'

interface Props {
  events: TimelineEvent[]
  currentStage: RepairStage
}

const STAGE_LABELS: Record<RepairStage, string> = {
  INITIALIZING:       'Initialize',
  RUNNING_TESTS:      'Run Tests',
  LOCALIZING_FAULT:   'Localize Fault',
  RETRIEVING_CONTEXT: 'Retrieve Context',
  GENERATING_PATCH:   'Generate Patches',
  VALIDATING_PATCH:   'Validate Patches',
  RANKING_PATCH:      'Rank Patches',
  COMPLETED:          'Completed',
}

const STAGE_ORDER: RepairStage[] = [
  'INITIALIZING',
  'RUNNING_TESTS',
  'LOCALIZING_FAULT',
  'RETRIEVING_CONTEXT',
  'GENERATING_PATCH',
  'VALIDATING_PATCH',
  'RANKING_PATCH',
  'COMPLETED',
]

function getStageStatus(stage: RepairStage, currentStage: RepairStage): 'done' | 'active' | 'pending' {
  const currentIdx = STAGE_ORDER.indexOf(currentStage)
  const stageIdx = STAGE_ORDER.indexOf(stage)
  if (stageIdx < currentIdx) return 'done'
  if (stageIdx === currentIdx) return 'active'
  return 'pending'
}

export default function RepairTimeline({ events, currentStage }: Props) {
  return (
    <div className="space-y-0">
      {STAGE_ORDER.map((stage, idx) => {
        const status = getStageStatus(stage, currentStage)
        const event = events.find(e => e.stage === stage)

        return (
          <div key={stage} className="flex gap-4">
            {/* Connector line + dot */}
            <div className="flex flex-col items-center">
              <div className={`
                w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 z-10
                ${status === 'done'   ? 'bg-green-700 text-green-100' : ''}
                ${status === 'active' ? 'bg-blue-600 text-white ring-2 ring-blue-400 ring-offset-2 ring-offset-gray-900' : ''}
                ${status === 'pending'? 'bg-gray-800 text-gray-500 border border-gray-700' : ''}
              `}>
                {status === 'done' ? '✓' : idx + 1}
              </div>
              {idx < STAGE_ORDER.length - 1 && (
                <div className={`w-0.5 flex-1 my-1 ${status === 'done' ? 'bg-green-700' : 'bg-gray-800'}`} />
              )}
            </div>

            {/* Label + message */}
            <div className="pb-5 pt-0.5">
              <p className={`text-sm font-semibold
                ${status === 'done'    ? 'text-green-400' : ''}
                ${status === 'active'  ? 'text-blue-300' : ''}
                ${status === 'pending' ? 'text-gray-600' : ''}
              `}>
                {STAGE_LABELS[stage]}
              </p>
              {event && (
                <p className="text-xs text-gray-500 mt-0.5">{event.message}</p>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

