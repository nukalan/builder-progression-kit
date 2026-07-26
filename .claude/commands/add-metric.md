---
description: Scaffold a new velocity metric test-first, following house conventions
argument-hint: [metric name and one-line definition]
---
New metric: $ARGUMENTS

Follow the house pattern strictly:
1. Add the metric definition to the Definitions section of CLAUDE.md (ask me to confirm wording).
2. Write the pytest test FIRST in dashboard/tests/test_metrics.py using plain dict fixtures — no network, no mocks of the GitHub client.
3. Run tests, confirm the new test fails for the right reason.
4. Implement as a pure function in dashboard/velocity/metrics.py (median not mean for durations, exclude records with missing fields, return 0.0 for empty input).
5. Run tests again; all green before you report done.
6. Add one line to dashboard/velocity/report.py to display it.
