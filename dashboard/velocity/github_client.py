"""Thin GitHub REST client. All network access lives here; metrics stay pure."""
from __future__ import annotations
import os
import requests

API = "https://api.github.com"


def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    h = {"Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fetch_merged_prs(repo: str, limit: int = 100) -> list[dict]:
    """Fetch recently closed PRs and keep the merged ones.

    Returns raw GitHub PR dicts (created_at, merged_at, number, ...).
    """
    prs: list[dict] = []
    page = 1
    while len(prs) < limit:
        r = requests.get(
            f"{API}/repos/{repo}/pulls",
            params={"state": "closed", "sort": "updated", "direction": "desc",
                    "per_page": 100, "page": page},
            headers=_headers(), timeout=30,
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        prs.extend(p for p in batch if p.get("merged_at"))
        page += 1
    return prs[:limit]


def fetch_reviews(repo: str, pr_number: int) -> list[dict]:
    """Fetch reviews for one PR (submitted_at, state, ...)."""
    r = requests.get(
        f"{API}/repos/{repo}/pulls/{pr_number}/reviews",
        headers=_headers(), timeout=30,
    )
    r.raise_for_status()
    return r.json()
