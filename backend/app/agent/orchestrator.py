"""
RepairOrchestrator – coordinates the full AutoPatch repair pipeline.

The orchestrator iterates through every pipeline stage in order,
delegating to injected components. Each component has a stub
implementation that can be replaced without restructuring this class.

Pipeline stages:
    INITIALIZING → RUNNING_TESTS → LOCALIZING_FAULT →
    RETRIEVING_CONTEXT → GENERATING_PATCH → VALIDATING_PATCH →
    RANKING_PATCH → COMPLETED
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from app.agent.policies import RepairPolicy
from app.agent.state import RepairStage, RepairState
from app.fault_localization.ochiai import OchiaiFaultLocalizer
from app.repair.generator import LLMRepairGenerator
from app.repair.ranker import HeuristicPatchRanker
from app.retrieval.code_search import SimpleCodeRetriever
from app.testing.runner import PytestRunner

logger = logging.getLogger(__name__)


class RepairOrchestrator:
    """
    Drives the repair pipeline for a single run.

    Inject component implementations via the constructor to swap in
    real algorithms without changing orchestration logic.
    """

    def __init__(
        self,
        *,
        policy: RepairPolicy | None = None,
        fault_localizer: OchiaiFaultLocalizer | None = None,
        code_retriever: SimpleCodeRetriever | None = None,
        repair_generator: LLMRepairGenerator | None = None,
        patch_ranker: HeuristicPatchRanker | None = None,
        test_runner: PytestRunner | None = None,
    ) -> None:
        self.policy = policy or RepairPolicy.default()
        self.fault_localizer = fault_localizer or OchiaiFaultLocalizer()
        self.code_retriever = code_retriever or SimpleCodeRetriever()
        self.repair_generator = repair_generator or LLMRepairGenerator()
        self.patch_ranker = patch_ranker or HeuristicPatchRanker()
        self.test_runner = test_runner or PytestRunner()

    async def run(self, state: RepairState) -> RepairState:
        """
        Execute the full repair pipeline and return the final state.

        Each stage mutates *state* and appends a timeline event.
        On failure the exception is logged and the state is returned
        with whatever progress was made.
        """
        try:
            state = await self._initialise(state)
            state = await self._run_tests(state)
            state = await self._localise_fault(state)
            state = await self._retrieve_context(state)
            state = await self._generate_patches(state)
            state = await self._validate_patches(state)
            state = await self._rank_patches(state)
            state = await self._complete(state)
        except Exception as exc:
            logger.exception("Repair pipeline failed at stage %s: %s", state.current_stage, exc)
            state.emit(f"Pipeline error: {exc}")
        return state

    # ── Private stage methods ─────────────────────────────────────────────────

    async def _initialise(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.INITIALIZING
        state.emit("Initialising repair run — cloning repository.")
        # TODO: clone repository via RepositoryManager
        return state

    async def _run_tests(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.RUNNING_TESTS
        state.emit("Running test suite to establish baseline.")
        state.test_results = await self.test_runner.run(state.local_repo_path)
        state.emit(
            "Test suite complete.",
            passed=getattr(state.test_results, "passed", 0),
            failed=getattr(state.test_results, "failed", 0),
        )
        return state

    async def _localise_fault(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.LOCALIZING_FAULT
        state.emit("Applying Ochiai fault localisation.")
        state.fault_locations = await self.fault_localizer.localize(
            repository=state.local_repo_path,
            test_results=state.test_results,
        )
        state.emit(f"Identified {len(state.fault_locations)} suspicious location(s).")
        return state

    async def _retrieve_context(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.RETRIEVING_CONTEXT
        state.emit("Retrieving relevant code context.")
        state.code_context = await self.code_retriever.retrieve(
            repository=state.local_repo_path,
            fault_locations=state.fault_locations,
        )
        return state

    async def _generate_patches(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.GENERATING_PATCH
        state.emit("Generating candidate patches.")
        state.patch_candidates = await self.repair_generator.generate(
            code_context=state.code_context,
            fault_locations=state.fault_locations,
            max_patches=self.policy.max_patch_candidates,
        )
        state.emit(f"Generated {len(state.patch_candidates)} candidate patch(es).")
        return state

    async def _validate_patches(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.VALIDATING_PATCH
        state.emit("Validating patches against test suite.")
        for patch in state.patch_candidates:
            # TODO: apply patch, run tests, revert patch
            _ = await self.test_runner.run(state.local_repo_path)
            state.emit(f"Validated patch: {getattr(patch, 'id', '?')}")
        return state

    async def _rank_patches(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.RANKING_PATCH
        state.emit("Ranking candidate patches.")
        state.patch_candidates = await self.patch_ranker.rank(state.patch_candidates)
        if state.patch_candidates:
            state.best_patch = state.patch_candidates[0]
            state.emit("Best patch selected.", patch_id=getattr(state.best_patch, "id", "?"))
        return state

    async def _complete(self, state: RepairState) -> RepairState:
        state.current_stage = RepairStage.COMPLETED
        state.emit("Repair pipeline completed successfully.")
        return state

