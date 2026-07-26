---
description: Structured self-review of the current uncommitted changes
---
Run `git diff` and review the current changes as a skeptical senior engineer. Check, in order:
1. Does every change comply with CLAUDE.md conventions (pure metrics, medians, type hints)?
2. Are there tests for new behavior, and do they test edge cases (empty list, missing fields, unmerged PRs)?
3. Timezone/parsing bugs in datetime handling?
4. Anything that silently changes a metric definition without updating CLAUDE.md?
5. Security: any secrets, tokens, or URLs hardcoded?

Output: a numbered list of findings ranked by severity, each with the file/line and a one-line fix. If clean, say so and list what you checked.
