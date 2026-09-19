# AutoPatch – Architecture

## Overview

AutoPatch is a monorepo containing three main components:

```
autopatch/
├── backend/    FastAPI application (Python)
├── frontend/   React + TypeScript SPA (Vite)
└── benchmark/  Benchmark repositories and issue descriptors
```

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Frontend                               │
│               React + TypeScript + Tailwind                     │
│  Dashboard │ New Repair │ Repair Run (pipeline + diff + tests)  │
└─────────────────────────────┬───────────────────────────────────┘
                              │  HTTP / REST
┌─────────────────────────────▼───────────────────────────────────┐
│                         Backend API                             │
│                     FastAPI + SQLAlchemy                        │
│  /api/health │ /api/issues │ /api/repair-runs │ /api/repositories│
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    Repair Orchestrator                          │
│   RepairOrchestrator coordinates the full pipeline              │
│   RepairState holds mutable pipeline state                      │
│   RepairPolicy configures run behaviour                         │
└──┬──────────┬────────────┬──────────┬──────────┬───────────────┘
   │          │            │          │          │
   ▼          ▼            ▼          ▼          ▼
Fault      Code         Repair    Test        Git/GitHub
Localizer  Retriever    Engine    Runner      Integration
(Ochiai)   (Simple)     (LLM)     (Pytest)    (API Client)
```

## Component Responsibilities

| Component | Module | Responsibility |
|---|---|---|
| API Layer | `app/api/` | HTTP routing, request validation, response serialisation |
| Services | `app/services/` | Business logic, database operations |
| Orchestrator | `app/agent/orchestrator.py` | Pipeline coordination |
| Fault Localizer | `app/fault_localization/` | Identify suspicious code locations |
| Code Retriever | `app/retrieval/` | Fetch relevant source context |
| Repair Generator | `app/repair/generator.py` | Generate candidate patches (LLM) |
| Patch Ranker | `app/repair/ranker.py` | Score and rank candidates |
| Test Runner | `app/testing/runner.py` | Execute test suite, collect results |
| Git Integration | `app/git/` | Clone, patch, diff, GitHub API |

## Data Flow

```
POST /api/repair-runs
        │
        ▼
RepairService.create_run()
        │
        ▼
RepairOrchestrator.run(state)
        │
        ├─ 1. INITIALIZING      → Clone repository
        ├─ 2. RUNNING_TESTS     → Execute baseline test suite
        ├─ 3. LOCALIZING_FAULT  → Compute Ochiai suspiciousness scores
        ├─ 4. RETRIEVING_CONTEXT→ Fetch code around fault locations
        ├─ 5. GENERATING_PATCH  → Call LLM to generate diffs
        ├─ 6. VALIDATING_PATCH  → Apply each patch, re-run tests
        ├─ 7. RANKING_PATCH     → Score patches by test pass + model score
        └─ 8. COMPLETED         → Return best patch for human review
```

## Database Schema (SQLite / SQLAlchemy)

```
issues
  id, title, description, repository_url, github_issue_url, created_at

repositories
  id, name, url, local_path, default_branch, created_at

repair_runs
  id, issue_id (FK), status, current_stage, started_at, completed_at

patch_candidates
  id, run_id (FK), description, diff, model_score, test_status, final_score, created_at

tool_calls
  id, run_id (FK), stage, name, input_data, output_data, timestamp
```

