# CLAUDE.md — Engineering Velocity Dashboard

## What this project is
A dashboard that pulls GitHub data and computes engineering velocity metrics:
PR cycle time, review turnaround, deployment frequency, and rework rate.
Built as a demonstration of a "builder progression" system: shared context,
command library, verification hooks, multi-model review, postmortem culture.

## Architecture
- `dashboard/velocity/github_client.py` — thin GitHub REST API client (requests, token from GITHUB_TOKEN env var)
- `dashboard/velocity/metrics.py` — pure functions: take PR/release dicts, return numbers. NO network calls here.
- `dashboard/velocity/report.py` — renders metrics to terminal + markdown report
- `dashboard/main.py` — CLI entry point, wires the above together
- `dashboard/tests/` — pytest; every metric has a test BEFORE it has an implementation

## Conventions
- Python 3.10+, type hints on all public functions
- Pure functions in metrics.py: input = list of dicts (already fetched), output = float/int. This keeps tests network-free.
- Timestamps: parse ISO 8601 from GitHub API with `datetime.fromisoformat(ts.replace("Z", "+00:00"))`
- Medians, not means, for all duration metrics (outlier PRs skew means)
- No new dependencies without asking. Current allowed: requests, pyyaml, pytest.

## Verification
Run after EVERY change (hooks do this automatically on file edits):
```
cd dashboard && python -m pytest tests/ -q
```
A change is not done until tests pass. If you add a metric, add its test first.

## Definitions (do not deviate without updating this file)
- **Cycle time**: PR created_at → merged_at, in hours. Unmerged PRs excluded.
- **Review turnaround**: PR created_at → first review submitted_at, in hours.
- **Deployment frequency**: merged PRs to default branch per week (proxy for deploys in a demo repo).
- **Rework rate**: fraction of merged PRs with commits pushed AFTER the first review (signal of review-driven churn).

## What NOT to do
- Do not add web frameworks. Output is terminal + markdown file. Keep it inspectable.
- Do not mock the GitHub API inside metrics tests — metrics are pure functions, feed them dicts.
- Do not "improve" metric definitions silently. Definitions are a contract; change them here first.
