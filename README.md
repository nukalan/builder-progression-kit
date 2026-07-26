# Builder Progression Kit + Engineering Velocity Dashboard

A working demonstration of an agentic "builder progression" system — the harness
that makes every AI-assisted build faster than the last — applied to a real
problem: measuring engineering velocity from GitHub data.

## The thesis
Teams that win with AI coding agents aren't the ones that use the tools — they're
the ones that build the **system around** the tools:

| Component | Where | What it does |
|---|---|---|
| Shared context | `CLAUDE.md` | Architecture, conventions, metric definitions — the contract every session loads |
| Command library | `.claude/commands/` | `/spec`, `/add-metric`, `/review-diff`, `/postmortem` — repeatable workflows, not ad-hoc prompts |
| Verification hooks | `.claude/settings.json` | pytest runs automatically after every agent edit — the agent catches its own failures |
| Permission tiers | `.claude/settings.json` | allow / ask / deny — tests auto-run, pushes ask, secrets are unreadable |
| Multi-model review | `scripts/three_model_review.sh` | Implementation model ≠ review model ≠ test-writer model |
| Postmortem culture | `postmortems/` | Every session ends by improving the harness, not just the code |

## The dashboard
Computes from the GitHub API: median PR cycle time, review turnaround,
deployment frequency, and rework rate. Medians over means; pure metric
functions; test-first. See `CLAUDE.md` for definitions.

```bash
cd dashboard
pip install -r requirements.txt
cp config.example.yaml config.yaml   # set your repo
export GITHUB_TOKEN=<fine-grained, read-only, single-repo>
python main.py                        # writes velocity_report.md
python -m pytest tests/ -q
```

## Why these metrics
Adoption counts and suggestion-acceptance rates look impressive and mean little.
Cycle time, review turnaround, and rework rate measure the learning loop: how
fast ideas reach production and how much churn the process adds. That's the
measurement philosophy this repo exists to demonstrate.
