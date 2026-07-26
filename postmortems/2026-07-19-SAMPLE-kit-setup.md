# Postmortem: Kit setup and first metric (SAMPLE — replace with your own)
**Date:** 2026-07-19 | **Session goal:** Stand up harness, implement cycle time metric

## What shipped
- Repo scaffold, CLAUDE.md v1, command library, hooks, cycle_time metric + tests

## What the agent got wrong (or needed correction)
- Used mean instead of median on first attempt → CLAUDE.md had no stated preference.
  Root cause: missing convention. Fixed by adding "medians, not means" to Conventions.

## Harness improvement made
- [x] CLAUDE.md updated: added median convention + datetime parsing recipe

## Evidence of compounding
- First metric took ~40 min including convention fixes; expectation: next metric
  under 15 min because pattern + conventions are now in context. Verify next session.
