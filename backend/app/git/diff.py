"""
Diff utilities.

Helpers for generating and formatting unified diffs between original
and patched source files.
"""

from __future__ import annotations

import difflib


def generate_diff(
    original: str,
    patched: str,
    fromfile: str = "original",
    tofile: str = "patched",
    context_lines: int = 3,
) -> str:
    """
    Generate a unified diff between two source strings.

    Args:
        original:      The original (buggy) source code as a string.
        patched:       The patched (fixed) source code as a string.
        fromfile:      Label for the original file in the diff header.
        tofile:        Label for the patched file in the diff header.
        context_lines: Number of unchanged lines to include around each hunk.

    Returns:
        A unified diff string (empty string if there are no differences).
    """
    original_lines = original.splitlines(keepends=True)
    patched_lines = patched.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        patched_lines,
        fromfile=fromfile,
        tofile=tofile,
        n=context_lines,
    )
    return "".join(diff)


def apply_diff_preview(original: str, diff: str) -> str:
    """
    Attempt to apply a unified diff to an original string in-memory.

    This is a best-effort preview only — not a production patch tool.
    For real patch application use `git apply` via the RepositoryManager.

    Returns:
        The patched string on success, or the original string on failure.
    """
    try:
        import patch as patch_lib  # type: ignore[import]
        patched = patch_lib.fromstring(diff.encode()).apply(original.encode())
        return patched.decode() if patched else original
    except Exception:
        # Fall back gracefully if the patch library is not available.
        return original

