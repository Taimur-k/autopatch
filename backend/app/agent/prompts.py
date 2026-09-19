"""
Prompt templates for the AutoPatch repair engine.

These are placeholder strings that will be populated with real context
and sent to an LLM once the AI repair engine is implemented.

Each template uses Python str.format()-style placeholders.
"""

from __future__ import annotations

# ── Fault localisation prompt ─────────────────────────────────────────────────
FAULT_LOCALIZATION_SYSTEM = """\
You are an expert software debugger specialising in automated program repair.
Given failing test output and suspicious code locations, identify the most
likely root cause of the bug.
"""

FAULT_LOCALIZATION_USER = """\
## Issue Description
{issue_description}

## Failing Tests
{failing_tests}

## Suspicious Locations (ranked by Ochiai score)
{fault_locations}

Analyse the evidence and identify the single most likely root cause.
"""

# ── Patch generation prompt ───────────────────────────────────────────────────
PATCH_GENERATION_SYSTEM = """\
You are an expert software engineer specialising in automated program repair.
Generate minimal, correct patches that fix the described bug without breaking
any existing functionality.
"""

PATCH_GENERATION_USER = """\
## Issue Description
{issue_description}

## Root Cause
{root_cause}

## Relevant Code
```python
{code_context}
```

## Failing Tests
{failing_tests}

Generate up to {max_patches} candidate patches as unified diffs.
Each patch must be minimal and targeted.
"""

# ── Patch ranking prompt ──────────────────────────────────────────────────────
PATCH_RANKING_SYSTEM = """\
You are a code review expert. Given a set of candidate patches for a bug,
rank them from most to least likely to be the correct, clean fix.
"""

PATCH_RANKING_USER = """\
## Issue
{issue_description}

## Candidate Patches
{patches}

Rank the patches and briefly justify your ranking.
"""

