"""CLI entry point: fetch data, compute metrics, render report."""
from __future__ import annotations
import argparse
import pathlib
import yaml

from velocity import github_client, metrics, report


def main() -> None:
    ap = argparse.ArgumentParser(description="Engineering velocity dashboard")
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    cfg = yaml.safe_load(pathlib.Path(args.config).read_text())
    repo = cfg["repo"]

    prs = github_client.fetch_merged_prs(repo, limit=30)

    reviews_by_pr = {pr["number"]: github_client.fetch_reviews(repo, pr["number"]) for pr in prs}

    results: dict[str, float | str] = {
        "Merged PRs analyzed": len(prs),
        "Median cycle time (hrs)": metrics.median_cycle_time_hours(prs),
        "Median review turnaround (hrs)": metrics.median_review_turnaround_hours(prs, reviews_by_pr),
    }
    out = report.render(repo, results)
    pathlib.Path("velocity_report.md").write_text(out)
    print("Saved velocity_report.md")


if __name__ == "__main__":
    main()
