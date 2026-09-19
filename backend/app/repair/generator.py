"""
LLM-based repair generator (stub implementation).

Implements RepairGenerator using an LLM to produce candidate patches.
Currently returns placeholder diffs so the pipeline can run end-to-end.

To implement:
1. Build the repair prompt from prompts.py using code_context + fault_locations.
2. Call the LLM API (OpenAI, Gemini, etc.).
3. Parse the response to extract unified diffs.
4. Return a list of PatchCandidate objects.
"""

from __future__ import annotations

import uuid
from typing import Any

from app.repair.base import PatchCandidate, RepairGenerator


class LLMRepairGenerator(RepairGenerator):
    """
    Generates candidate patches by prompting a large language model.

    TODO: Connect to a real LLM API using the prompt templates in
          app/agent/prompts.py.
    """

    async def generate(
        self,
        code_context: str,
        fault_locations: list[Any],
        max_patches: int = 5,
    ) -> list[PatchCandidate]:
        """
        Return placeholder patches.

        Replace this body with real LLM calls once the AI engine is wired up.
        """
        # ── Placeholder patches ────────────────────────────────────────────
        placeholders = [
            PatchCandidate(
                id=str(uuid.uuid4()),
                description="Fix off-by-one error in boundary check.",
                diff=(
                    "--- a/src/parser.py\n"
                    "+++ b/src/parser.py\n"
                    "@@ -40,7 +40,7 @@\n"
                    "     if index >= len(tokens):\n"
                    "-        raise IndexError('index out of range')\n"
                    "+        return None\n"
                ),
                model_score=0.88,
            ),
            PatchCandidate(
                id=str(uuid.uuid4()),
                description="Add None guard to process_request.",
                diff=(
                    "--- a/src/service.py\n"
                    "+++ b/src/service.py\n"
                    "@@ -86,6 +86,8 @@\n"
                    " def process_request(req):\n"
                    "+    if req is None:\n"
                    "+        return {}\n"
                    "     data = req.data\n"
                ),
                model_score=0.74,
            ),
            PatchCandidate(
                id=str(uuid.uuid4()),
                description="Initialise result before conditional assignment.",
                diff=(
                    "--- a/src/utils.py\n"
                    "+++ b/src/utils.py\n"
                    "@@ -15,6 +15,7 @@\n"
                    " def validate(value):\n"
                    "+    result = None\n"
                    "     if value:\n"
                    "         result = value.strip()\n"
                ),
                model_score=0.61,
            ),
        ]
        return placeholders[:max_patches]

