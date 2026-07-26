#!/usr/bin/env bash
# Three-model review workflow:
#   Model 1 (Claude Code) implemented the change.
#   Model 2 (e.g. ChatGPT/Codex) — adversarial reviewer.
#   Model 3 (e.g. Gemini) — writes tests from the spec, blind to the implementation.
# This script packages the diff + prompts; paste into the other models' UIs.
set -euo pipefail
BASE="${1:-main}"
OUT="review_packets"
mkdir -p "$OUT"
DIFF_FILE="$OUT/diff_vs_${BASE}.patch"
git diff "$BASE" > "$DIFF_FILE"
LINES=$(wc -l < "$DIFF_FILE")
echo "Diff vs '$BASE' captured: $DIFF_FILE ($LINES lines)"

cat > "$OUT/prompt_model2_reviewer.md" << 'P2'
You are an adversarial senior code reviewer. Below is a unified diff. Find real
problems only — no style nitpicks. Focus on: logic errors, edge cases (empty
input, missing fields, timezone handling), silent behavior changes, and test
gaps. For each finding: severity (HIGH/MED/LOW), file, line, one-line fix.
If you find nothing HIGH, say so explicitly.
--- DIFF BELOW ---
P2
cat "$DIFF_FILE" >> "$OUT/prompt_model2_reviewer.md"

cat > "$OUT/prompt_model3_testwriter.md" << 'P3'
Without seeing the implementation, write pytest test cases for this spec.
Cover: happy path, empty input, records with missing fields, and one boundary
case. Tests take plain Python dicts as input (no network, no mocks).
--- SPEC BELOW (paste the relevant Definitions section from CLAUDE.md) ---
P3

echo "Packets ready in $OUT/:"
echo "  1. prompt_model2_reviewer.md  -> paste into reviewer model"
echo "  2. prompt_model3_testwriter.md -> add spec, paste into test-writer model"
echo "Log outcomes (caught something real? pure ceremony?) in your postmortem."
