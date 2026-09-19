// ── Core domain types mirroring the backend Pydantic schemas ─────────────────

export interface Issue {
  id: string
  title: string
  description: string
  repository_url: string
  github_issue_url: string | null
  created_at: string
}

export interface Repository {
  id: string
  name: string
  url: string
  local_path: string | null
  default_branch: string
  created_at: string
}

export type RepairStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED'

export type RepairStage =
  | 'INITIALIZING'
  | 'RUNNING_TESTS'
  | 'LOCALIZING_FAULT'
  | 'RETRIEVING_CONTEXT'
  | 'GENERATING_PATCH'
  | 'VALIDATING_PATCH'
  | 'RANKING_PATCH'
  | 'COMPLETED'

export interface RepairRun {
  id: string
  issue_id: string
  status: RepairStatus
  current_stage: RepairStage
  started_at: string
  completed_at: string | null
}

export interface TimelineEvent {
  timestamp: string
  stage: RepairStage
  message: string
  metadata: Record<string, unknown> | null
}

export interface FaultLocation {
  file: string
  line: number
  function: string | null
  suspiciousness_score: number
}

export type TestStatus = 'PENDING' | 'PASSED' | 'FAILED' | 'ERROR'

export interface PatchCandidate {
  id: string
  description: string
  diff: string
  model_score: number
  test_status: TestStatus
  final_score: number
}

export interface HealthResponse {
  status: string
  version: string
  uptime_seconds: number
  timestamp: string
}

