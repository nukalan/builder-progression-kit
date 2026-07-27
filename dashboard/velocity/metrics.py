"""Pure metric functions. Input: lists of dicts. Output: numbers. No network.

House rules (see CLAUDE.md): medians not means; exclude records with missing
fields; empty input returns 0.0.
"""
from __future__ import annotations
from datetime import datetime
from statistics import median


def _parse(ts: str) -> datetime:
    """Parse a GitHub ISO-8601 timestamp like '2026-07-01T12:30:00Z'.

    Example:
        >>> _parse('2026-07-01T12:30:00Z')
        datetime.datetime(2026, 7, 1, 12, 30, tzinfo=datetime.timezone.utc)
    """
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def median_cycle_time_hours(prs: list[dict]) -> float:
    """Median hours from PR created_at to merged_at.

    REFERENCE IMPLEMENTATION — this is the house pattern. Every other metric
    should look like this: guard empty input, skip incomplete records, median.
    """
    durations = []
    for pr in prs:
        created, merged = pr.get("created_at"), pr.get("merged_at")
        if not created or not merged:
            continue
        durations.append((_parse(merged) - _parse(created)).total_seconds() / 3600)
    return round(median(durations), 2) if durations else 0.0


def median_review_turnaround_hours(prs: list[dict], reviews_by_pr: dict[int, list[dict]]) -> float:
    """Median hours from PR created_at to FIRST review submitted_at.

    TODO(you + Claude Code): implement via /add-metric. See BUILD_PLAN.md step 3.
    Spec: for each PR, find earliest review 'submitted_at'; skip PRs with no
    reviews; median over hours; 0.0 for empty.
    """
    raise NotImplementedError("Build this with /add-metric — see BUILD_PLAN.md")


def deployment_frequency_per_week(prs: list[dict], weeks: int) -> float:
    """Merged PRs to default branch per week over the window.

    TODO(you + Claude Code): implement via /add-metric.
    """
    raise NotImplementedError("Build this with /add-metric — see BUILD_PLAN.md")


def rework_rate(prs: list[dict], reviews_by_pr: dict[int, list[dict]],
                commits_by_pr: dict[int, list[dict]]) -> float:
    """Fraction of merged PRs with commits AFTER the first review.

    TODO(you + Claude Code): hardest one — you'll need to add a commits fetcher
    to github_client.py too. Do it last.
    """
    raise NotImplementedError("Build this with /add-metric — see BUILD_PLAN.md")
