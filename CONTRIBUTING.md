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

1. **Open an issue first.** Describe which system and why it meets the [curation criteria](README.md#curation-criteria)
2. Once approved, PR must include:
   - Full row data for ALL comparison categories
   - Source links for every ✅ claim
   - GitHub stars and metadata
3. One system per PR

### Adding a new comparison row

1. Open an issue proposing the new dimension
2. Provide source links for ALL listed systems in that dimension
3. One row per PR

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
- New systems: reviewed within 1 week
- Maintainer corrections: fast-track (usually same day)
- PRs without source links: asked to provide them before review

## Conduct

Assume good faith. This table exists to help developers choose tools, not to attack projects. Corrections improve accuracy for everyone.
