"""Metric tests. Pure dict fixtures — no network, no mocks. House rule."""
import pytest
from velocity import metrics


def pr(created: str, merged: str | None) -> dict:
    return {"created_at": created, "merged_at": merged}


# ---------- median_cycle_time_hours (reference metric: implemented) ----------

def test_cycle_time_basic():
    prs = [
        pr("2026-07-01T00:00:00Z", "2026-07-01T10:00:00Z"),  # 10h
        pr("2026-07-02T00:00:00Z", "2026-07-03T00:00:00Z"),  # 24h
        pr("2026-07-04T00:00:00Z", "2026-07-04T02:00:00Z"),  # 2h
    ]
    assert metrics.median_cycle_time_hours(prs) == 10.0


def test_cycle_time_skips_unmerged_and_handles_empty():
    assert metrics.median_cycle_time_hours([]) == 0.0
    prs = [pr("2026-07-01T00:00:00Z", None),
           pr("2026-07-01T00:00:00Z", "2026-07-01T06:00:00Z")]
    assert metrics.median_cycle_time_hours(prs) == 6.0


# ---------- specs for the metrics YOU will implement with Claude Code --------
# Un-skip each test as you implement its metric (BUILD_PLAN.md steps 3-5).

# ---------- median_review_turnaround_hours (implementing) ----------

def test_review_turnaround_basic():
    prs = [
        {"number": 1, "created_at": "2026-07-01T00:00:00Z"}, # 8h
        {"number": 2, "created_at": "2026-07-01T00:00:00Z"}, # 24h
        {"number": 3, "created_at": "2026-07-01T00:00:00Z"}, # 2h
    ]
    reviews = {
        1: [{"submitted_at": "2026-07-01T08:00:00Z"}],
        2: [{"submitted_at": "2026-07-02T00:00:00Z"}],
        3: [{"submitted_at": "2026-07-01T02:00:00Z"}],
    }
    # Median of [8, 24, 2] is 8
    assert metrics.median_review_turnaround_hours(prs, reviews) == 8.0


def test_review_turnaround_uses_first_review():
    prs = [{"number": 1, "created_at": "2026-07-01T00:00:00Z"}]
    reviews = {1: [{"submitted_at": "2026-07-01T20:00:00Z"},
                   {"submitted_at": "2026-07-01T08:00:00Z"}]} # first review was 8h later
    assert metrics.median_review_turnaround_hours(prs, reviews) == 8.0


def test_review_turnaround_skips_unreviewed_and_handles_empty():
    assert metrics.median_review_turnaround_hours([], {}) == 0.0
    prs = [
        {"number": 1, "created_at": "2026-07-01T00:00:00Z"}, # 10h
        {"number": 2, "created_at": "2026-07-01T00:00:00Z"}, # no review
    ]
    reviews = {1: [{"submitted_at": "2026-07-01T10:00:00Z"}]}
    assert metrics.median_review_turnaround_hours(prs, reviews) == 10.0


@pytest.mark.skip(reason="Step 4: implement deployment_frequency_per_week via /add-metric")
def test_deployment_frequency():
    prs = [{"merged_at": f"2026-07-0{d}T12:00:00Z", "created_at": "2026-07-01T00:00:00Z"}
           for d in (1, 2, 3, 4)]
    assert metrics.deployment_frequency_per_week(prs, weeks=2) == 2.0


@pytest.mark.skip(reason="Step 5: implement rework_rate via /add-metric (hardest)")
def test_rework_rate():
    prs = [{"number": 1, "created_at": "2026-07-01T00:00:00Z", "merged_at": "2026-07-03T00:00:00Z"},
           {"number": 2, "created_at": "2026-07-01T00:00:00Z", "merged_at": "2026-07-03T00:00:00Z"}]
    reviews = {1: [{"submitted_at": "2026-07-01T10:00:00Z"}],
               2: [{"submitted_at": "2026-07-01T10:00:00Z"}]}
    commits = {1: [{"commit": {"committer": {"date": "2026-07-02T00:00:00Z"}}}],  # after review -> rework
               2: [{"commit": {"committer": {"date": "2026-07-01T05:00:00Z"}}}]}  # before review
    assert metrics.rework_rate(prs, reviews, commits) == 0.5
