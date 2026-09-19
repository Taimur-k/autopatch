"""
Repair policy configuration.

RepairPolicy controls the behaviour of a single repair run:
how many patches to generate, timeouts, approval mode, etc.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.config import settings


@dataclass
class RepairPolicy:
    """
    Configures the behaviour of the RepairOrchestrator for one run.

    Attributes:
        max_patch_candidates:   Maximum number of patches to generate.
        validation_timeout_sec: Seconds to wait for test-suite validation.
        auto_approve:           If True, the best patch is applied without
                                human review (only safe in automated benchmarks).
        max_fault_locations:    How many fault locations to pass to the
                                repair generator.
        temperature:            Sampling temperature for the LLM (future use).
    """

    max_patch_candidates: int = field(
        default_factory=lambda: settings.MAX_PATCH_CANDIDATES
    )
    validation_timeout_sec: int = field(
        default_factory=lambda: settings.PATCH_VALIDATION_TIMEOUT
    )
    auto_approve: bool = field(
        default_factory=lambda: settings.AUTO_APPROVE_PATCH
    )
    max_fault_locations: int = 5
    temperature: float = 0.2

    @classmethod
    def default(cls) -> "RepairPolicy":
        """Return a policy with all defaults from application settings."""
        return cls()

    @classmethod
    def aggressive(cls) -> "RepairPolicy":
        """Return a policy that generates more patches with higher temperature."""
        return cls(
            max_patch_candidates=10,
            temperature=0.7,
            max_fault_locations=10,
        )

