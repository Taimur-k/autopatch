import axios from 'axios'
import type {
  FaultLocation,
  HealthResponse,
  Issue,
  PatchCandidate,
  RepairRun,
  Repository,
  TimelineEvent,
} from '../types'

// Axios instance — all requests go to /api (proxied to backend in dev).
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// ── Health ────────────────────────────────────────────────────────────────────

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>('/health')
  return data
}

// ── Issues ────────────────────────────────────────────────────────────────────

export interface CreateIssuePayload {
  title: string
  description: string
  repository_url: string
  github_issue_url?: string
}

export async function createIssue(payload: CreateIssuePayload): Promise<Issue> {
  const { data } = await api.post<Issue>('/issues', payload)
  return data
}

export async function getIssue(issueId: string): Promise<Issue> {
  const { data } = await api.get<Issue>(`/issues/${issueId}`)
  return data
}

// ── Repositories ──────────────────────────────────────────────────────────────

export interface CreateRepositoryPayload {
  name: string
  url: string
  default_branch?: string
}

export async function createRepository(payload: CreateRepositoryPayload): Promise<Repository> {
  const { data } = await api.post<Repository>('/repositories', payload)
  return data
}

export async function getRepository(repoId: string): Promise<Repository> {
  const { data } = await api.get<Repository>(`/repositories/${repoId}`)
  return data
}

// ── Repair Runs ───────────────────────────────────────────────────────────────

export async function createRepairRun(issueId: string): Promise<RepairRun> {
  const { data } = await api.post<RepairRun>('/repair-runs', { issue_id: issueId })
  return data
}

export async function getRepairRun(runId: string): Promise<RepairRun> {
  const { data } = await api.get<RepairRun>(`/repair-runs/${runId}`)
  return data
}

export async function getTimeline(runId: string): Promise<TimelineEvent[]> {
  const { data } = await api.get<TimelineEvent[]>(`/repair-runs/${runId}/timeline`)
  return data
}

export async function getFaultLocations(runId: string): Promise<FaultLocation[]> {
  const { data } = await api.get<FaultLocation[]>(`/repair-runs/${runId}/fault-locations`)
  return data
}

export async function getPatches(runId: string): Promise<PatchCandidate[]> {
  const { data } = await api.get<PatchCandidate[]>(`/repair-runs/${runId}/patches`)
  return data
}

