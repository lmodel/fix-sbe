"""Shared pytest fixtures for the fix-sbe test suite."""
from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def fix_record_tally(request):
    """Session-scoped accumulator for SBE record counts across third-party files.

    Tests add to ``tally["total"]`` as they validate each upstream XML/YAML
    fixture; the cumulative total is printed at session teardown so the
    corpus-wide processing volume is visible alongside per-file output.
    """
    tally: dict[str, int] = {"total": 0}

    def _report() -> None:
        reporter = request.config.pluginmanager.get_plugin("terminalreporter")
        msg = f"fix-sbe third-party records validated: {tally['total']}"
        if reporter is not None:
            reporter.write_sep("-", msg)
        else:
            print(msg)

    request.addfinalizer(_report)
    return tally
