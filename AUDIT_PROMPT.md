# Audit a Memory System for ai-memory-comparison

You are auditing **[SYSTEM_NAME]** ([GITHUB_URL]) for the open-source comparison table at https://github.com/carsteneu/ai-memory-comparison

## What to do

1. **Read the system's README, docs, and source code** at [GITHUB_URL]
2. **Check each feature below** against the criteria defined in https://github.com/carsteneu/ai-memory-comparison/blob/main/CRITERIA.md
3. **For every ✅ claim** you make, find the **exact source evidence**: file path + line number (or docs section) that proves the feature exists
4. **Create an evidence file** following the format in https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/_TEMPLATE.md
5. **Output the result** as a complete evidence file (copy-paste ready), plus a summary of what changed vs. the current table

## Rules

- **If it's not publicly documented → ❌** (no assumptions, no "probably has it")
- **Code beats docs** — if docs claim it but the code doesn't implement it → ❌
- **At least one citation per ✅** — file path + line number or docs anchor link
- **Use GitHub permalinks** (commit hash, not `main`) for permanent citations
- **State clearly what you COULDN'T verify** — better honest ❌ than a wrong ✅

## Current table entry for reference

Look at https://github.com/carsteneu/ai-memory-comparison/blob/main/data.js and find the entry with `id: "[SYSTEM_ID]"`. This is what the table currently claims. **Your job is to verify or correct every single field.**

## Output format

1. An **evidence file** at `evidence/[system-id].md` (ready to commit)
2. A **summary** of corrections: what changed from ❌ to ✅ (with citations), what changed from ✅ to ❌ (with reasons)

## Time budget

Spend max 15 minutes. Focus on finding definitive source evidence, not reading every line of code. Use `grep`, GitHub code search, and the README/docs. If you can't find evidence for a feature in 2 minutes of searching, mark it ❌.
