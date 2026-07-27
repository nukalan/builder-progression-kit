# Postmortem: Review Turnaround & PR Capping
**Date:** 2026-07-26 | **Session goal:** Implement review turnaround metric and optimize API call volume.

## What shipped
- Implemented `median_review_turnaround_hours` as a pure function in `metrics.py`.
- Added comprehensive unit tests for the new metric in `test_metrics.py`.
- Wired the metric into the main CLI reporting loop in `main.py`.
- Capped the analysis window to the 30 most recent merged PRs to prevent API hammering.

## What the agent got wrong (or needed correction)
- **CWD confusion** → Tried to `cd dashboard` while already inside the `dashboard` directory, resulting in a shell error. Root cause: failure to accurately track session CWD.
- **Over-engineering** → Proposed a GraphQL bulk-fetch implementation to solve the N+1 review problem. The user corrected this, emphasizing "simpler beats clever" for a demo tool. Root cause: misjudged the balance between "demonstration" and "production-grade" optimization.

## Harness improvement made
- [ ] CLAUDE.md updated: Added "Simplicity over optimization" guideline.
- [ ] Command added/edited: N/A
- [ ] Hook/permission changed: N/A

## Evidence of compounding
The implementation of the metric followed the "house pattern" perfectly (test-first, pure function, median logic) without needing guidance, showing that the reference implementation and `CLAUDE.md` patterns are successfully compounding.
