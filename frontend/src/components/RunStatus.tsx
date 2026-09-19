import type { RepairStatus } from '../types'

interface Props {
  status: RepairStatus
}

const CONFIG: Record<RepairStatus, { label: string; className: string }> = {
  PENDING:   { label: 'Pending',   className: 'bg-gray-700 text-gray-300' },
  RUNNING:   { label: 'Running',   className: 'bg-blue-900 text-blue-300 animate-pulse' },
  COMPLETED: { label: 'Completed', className: 'bg-green-900 text-green-300' },
  FAILED:    { label: 'Failed',    className: 'bg-red-900 text-red-300' },
  CANCELLED: { label: 'Cancelled', className: 'bg-yellow-900 text-yellow-300' },
}

export default function RunStatus({ status }: Props) {
  const { label, className } = CONFIG[status] ?? CONFIG.PENDING
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold ${className}`}>
      {label}
    </span>
  )
}

