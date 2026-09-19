# AutoPatch – Repair Workflow

This document describes the step-by-step repair workflow that AutoPatch
will execute for each bug report.

## Full Pipeline

```
Bug Report / GitHub Issue
          │
          ▼
  ┌───────────────────┐
  │  Repository Setup │   Clone repo, set up sandbox environment
  └────────┬──────────┘
           │
           ▼
  ┌───────────────────┐
  │    Run Tests      │   Establish baseline: identify failing tests
  └────────┬──────────┘
           │
           ▼
  ┌───────────────────────────┐
  │    Fault Localisation     │   Ochiai SBFL on coverage matrix
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Rank Suspicious Code     │   Sort by suspiciousness score
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Retrieve Code Context    │   Extract code around fault locations
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Generate Candidate       │   LLM produces N unified diffs
  │  Patches                  │
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Validate Patches         │   Apply each patch, re-run test suite
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Rank Patches             │   Score by (model confidence + test pass)
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Select Best Valid Patch  │
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Show Diff to User        │   Human review in the UI
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Human Approval           │   ✓ Approve  /  ✗ Reject
  └────────┬──────────────────┘
           │
           ▼
  ┌───────────────────────────┐
  │  Create GitHub PR         │   Auto-submit patch as a pull request
  └───────────────────────────┘
```

## Stage Details

### 1. Repository Setup
- Clone the target repository to a temporary sandbox directory.
- Check out the relevant branch/commit.
- Record the `local_path` in the `repositories` table.

### 2. Run Tests
- Execute the full test suite using `PytestRunner`.
- Collect pass/fail/error/skip counts and per-test outcomes.
- This forms the baseline; failing tests are the fault signal.

### 3. Fault Localisation
- Use `OchiaiFaultLocalizer` to compute per-statement suspiciousness.
- Requires a coverage matrix: which tests execute which statements.
- Sort locations by score descending.

### 4. Retrieve Code Context
- For each top-N fault location, extract the enclosing function body.
- Optionally include caller/callee context via call-graph analysis.
- Assemble into a formatted string for the LLM prompt.

### 5. Generate Candidate Patches
- Build prompt from `prompts.py` templates.
- Call LLM API (GPT-4o, Gemini, etc.).
- Parse response to extract unified diffs.
- Generate up to `policy.max_patch_candidates` patches.

### 6. Validate Patches
- For each candidate: apply the diff, run the full test suite, revert.
- Record `test_status` (PASSED / FAILED / ERROR) on the `PatchCandidate`.

### 7. Rank Patches
- `HeuristicPatchRanker` combines `model_score` and `test_status`.
- Future: add AST complexity, code naturalness, semantic similarity.

### 8. Human Review
- The best valid patch is shown as a diff in the UI.
- User clicks Approve → AutoPatch commits the patch and opens a GitHub PR.

