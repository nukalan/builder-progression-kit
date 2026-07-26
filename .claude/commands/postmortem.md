---
description: Generate a postmortem entry for the work session just completed
---
Look at `git log --oneline -15` and the conversation so far. Draft a postmortem entry
following postmortems/TEMPLATE.md, covering this session:
1. What was built.
2. Where the agent (you) went wrong or needed correction — be honest and specific.
3. What context was missing that, if added to CLAUDE.md or a command, would prevent it next time.
4. Proposed CLAUDE.md diff (if any).

Save it as postmortems/YYYY-MM-DD-<slug>.md with today's date. Do not commit it; I review first.
