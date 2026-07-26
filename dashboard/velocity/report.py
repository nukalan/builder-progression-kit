"""Render metrics to terminal and a markdown report file."""
from __future__ import annotations


def render(repo: str, results: dict[str, float | str]) -> str:
    lines = [f"# Engineering Velocity — {repo}", ""]
    lines += [f"- **{name}**: {value}" for name, value in results.items()]
    report = "\n".join(lines) + "\n"
    print(report)
    return report
