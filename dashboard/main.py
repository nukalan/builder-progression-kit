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

    prs = github_client.fetch_merged_prs(repo)
    results: dict[str, float | str] = {
        "Merged PRs analyzed": len(prs),
        "Median cycle time (hrs)": metrics.median_cycle_time_hours(prs),
        # TODO(you): wire in review turnaround, deployment frequency, rework rate
        # as you implement them. Reviews fetch (N+1 calls) is intentionally left
        # for you to design — batching decision is a good /spec exercise.
    }
    out = report.render(repo, results)
    pathlib.Path("velocity_report.md").write_text(out)
    print("Saved velocity_report.md")


if __name__ == "__main__":
    main()
