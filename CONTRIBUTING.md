# Contributing

Every claim in the comparison table must be verifiable. That's the only rule that matters.

## How to contribute

### Correcting a row (most common)

1. Find the row you want to correct in [comparison.md](comparison.md)
2. Open a PR changing the ❌ to ✅ (or vice versa)
3. In the PR description, link to the **public source** that proves the correction:
   - README section
   - Documentation page
   - Source code file + line
4. No source link = PR will be asked for one before review

### Adding a new system

Submit a PR directly — no need to open an issue first. The PR must include:

1. **An evidence file** at `evidence/<system-id>.md`, using the [evidence template](evidence/_TEMPLATE.md)
   - Fill in every feature: ✅ with source citations or ❌
   - The template lists all 79 features — work through them systematically
   - For each ✅, link to the exact file + line on GitHub (README, docs, or source code)
   - For ❌, just leave the ❌ — no source needed
2. **One system per PR**

The maintainers will create the `data.js` entry from your evidence file.

> **Tip:** Use the [evidence template](evidence/_TEMPLATE.md) as your starting point. It has every feature pre-listed with space for citations.

### Adding a new comparison row

Handled by maintainers — adding a feature requires sourcing every row in the table. If you have a suggestion, mention it in any PR or issue discussion. Maintainers will evaluate scope and feasibility.

### Fixing a broken source link

Open a PR with the corrected link. Fast-track review.

## Source quality

Acceptable sources:
- Project README
- Official documentation (`docs.`, `help.`, GitHub Pages)
- Source code (link to file + line on GitHub)
- Published benchmarks with methodology

Not acceptable:
- Twitter/X threads
- Discord messages
- Blog posts (unless linked from official docs)
- "I used it and it has this feature"

## For project maintainers

If your project is listed here and something is wrong:

1. **Open a PR.** Maintainer corrections get priority review.
2. Include source links. Even maintainers need to show where the feature is documented.
3. Adding features to your project so you can claim the ✅? **Go for it.** That's the point — this table should drive the ecosystem forward.

## Review process

- Corrections with clear source links: usually merged within 48 hours
- New system PRs with complete evidence file: reviewed within 1 week
- Maintainer corrections: fast-track (usually same day)
- PRs without source links: asked to provide them before review

## Conduct

Assume good faith. This table exists to help developers choose tools, not to attack projects. Corrections improve accuracy for everyone.
