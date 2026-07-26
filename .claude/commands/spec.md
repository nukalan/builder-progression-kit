---
description: Turn a one-line idea into a reviewed implementation plan before any code is written
argument-hint: [one-line description of the feature]
---
Feature idea: $ARGUMENTS

Before writing ANY code, produce a short spec:
1. Restate the goal in one sentence.
2. Which files change (per the architecture in CLAUDE.md)?
3. Exact function signature(s) with type hints.
4. The test cases that will prove it works (inputs → expected outputs, including one edge case).
5. What is explicitly OUT of scope.

Then STOP and wait for my approval before implementing.
