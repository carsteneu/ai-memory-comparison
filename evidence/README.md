# Evidence Directory

Every ✅ in the comparison table must be backed by a citation to public source code or documentation.

## Format

Each system has a file `evidence/<system-id>.md`:

```markdown
## System Name — Evidence

### Feature Name ✅
- `path/to/file.go:42` — what the code/docs prove
- `docs/feature.md#section` — additional context if needed

### Feature Name ❌
- Not found in public documentation or source code
```

## Rules

1. **One citation minimum** per ✅. At least one link to a specific file and line number, or a documentation section.
2. **Code wins over docs.** If docs claim a feature but the code doesn't implement it → ❌.
3. **No inference.** "The architecture implies they could do X" → ❌. Must be implemented.
4. **GitHub permalinks preferred.** Link to a specific commit hash, not `main`, so citations don't rot.

## Contributing

If your system is listed and you want to correct a ❌:
1. Submit a PR adding the evidence citation
2. If the feature was recently added, the citation must point to a merged commit
