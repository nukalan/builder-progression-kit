# BUILD PLAN — Your hands-on work (delete this file before making the repo public)

The scaffold gives you the harness + one reference metric. **You** build the rest
with Claude Code. The point is the practice AND an authentic commit history.
Budget: ~2 sessions of 2–3 hours. Log a postmortem after each session.

## Step 0 — Stand it up (15 min)
```bash
cd ~/dev/interview-prep
unzip builder-progression-kit.zip && cd builder-progression-kit
git init && git add -A && git commit -m "Scaffold: harness + reference metric"
cd dashboard && pip install -r requirements.txt && python -m pytest tests/ -q
# expect: 2 passed, 3 skipped
```
Create a GitHub repo, push. Then create a fine-grained GitHub token:
github.com → Settings → Developer settings → Fine-grained tokens → scope it to
READ-ONLY on this ONE repo. `export GITHUB_TOKEN=...` (never commit it).

## Step 1 — First contact with the harness (20 min)
Start `claude` in the repo root. Try, in order:
1. Ask: "Read CLAUDE.md and summarize the house rules in 3 bullets." (confirms context loads)
2. Run `/review-diff` (should report clean and list what it checked)
3. Make a trivial edit via Claude ("add a docstring example to _parse") and
   WATCH THE HOOK fire pytest automatically after the edit. That auto-verification
   moment is a beat in your demo — remember it.

## Step 2 — Point it at real data (30 min)
- `cp config.example.yaml config.yaml`, set a repo with real PR history
  (a busy public repo works; your own is better for the demo).
- Run `python main.py`. You should get a real median cycle time.
- Commit: "Live data: cycle time against <repo>".

## Step 3 — Build review turnaround WITH the command library (45 min)
In Claude Code:
```
/add-metric review turnaround — median hours from PR creation to first review
```
The command forces the house workflow: definition → test first → fail → implement
→ green → report line. Un-skip `test_review_turnaround_uses_first_review` as part
of it. You must also wire fetching reviews into main.py — use `/spec` first:
```
/spec wire review fetching into main.py without N+1 calls for repos with many PRs
```
(Claude will propose something; push back at least once — e.g. cap fetches at 30
PRs. Deciding the tradeoff is YOUR judgment call. That's the demo story.)
Commit. Write postmortem #1 with `/postmortem`: what did the agent get wrong,
what did you add to CLAUDE.md?

## Step 4 — Deployment frequency (20 min — should feel FAST)
```
/add-metric deployment frequency — merged PRs to default branch per week
```
Time yourself. If step 3 took 45 min and this takes 15, you have your
"compounding speed" evidence — write the numbers in postmortem #2.

## Step 5 — Rework rate (45 min, hardest)
Needs a new fetcher in github_client.py (PR commits) + timestamp comparison vs
first review. Use `/spec` first, then `/add-metric`. This one WILL surface an
agent mistake (timezone or ordering bugs are common). Perfect postmortem fodder.

## Step 6 — Three-model review (30 min)
On the rework-rate diff before merging:
```bash
./scripts/three_model_review.sh main
```
Paste packet 2 into ChatGPT/Codex, packet 3 into Gemini. Record honestly in the
postmortem: did cross-model review catch anything real, or was it ceremony for
a diff this size? Your calibrated answer IS the interview answer.

## Step 7 — Polish for the demo (30 min)
- Delete this file and the SAMPLE postmortem. Your real postmortems stay.
- README screenshot/paste of a real velocity_report.md.
- Rehearse the 10-min demo:
  1. CLAUDE.md — "context before code" (1 min)
  2. Live: `/add-metric` something small, hooks fire, tests gate it (4 min)
  3. Real report + your measurement philosophy over it (3 min)
  4. Postmortems — show the timing numbers proving compounding speed (2 min)

## Prompting discipline throughout
- Small asks, verify each. Never accept a diff you haven't read.
- When Claude gets something wrong: fix the HARNESS (CLAUDE.md/commands), not
  just the code. That habit is the whole thesis of the kit.
- Commit after every green step with honest messages.
