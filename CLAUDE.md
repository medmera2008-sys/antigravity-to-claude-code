# Sovereign Code Constitution & Invariants for Claude Code (CLAUDE.md)

## Code Hygiene & Language Invariants
- Zero-Unbound State: Pre-initialize variables before branching; exhaustive else fallback required.
- Defensive Access: Verify object/slice existence with safe navigation (.get, ?., nil checks).
- Anti-Overengineering: Three-Line Rule. Bug fixes prefer deletion over addition (net-negative diffs).
- Comments: Default ZERO comments. Never explain WHAT code does.
- Anti-Masking: Trust internal invariants; fail fast. Validate only at external system boundaries.
- Blast Radius: Run git status before destructive operations. Never use `git add .` blindly.
- Removed-Behavior: Before deleting lines, audit what invariant they enforced.
- Mandatory Verification: Pre-flight syntax validation (`python3 -m py_compile`, `node --check`, `cargo check`).

## Swarm Delegation Invariants
- Never delegate understanding: Provide exact paths, lines, and targets to subagents.
- Workspace Isolation: Use isolated git worktrees for concurrent edits.
- Conclusion-Only Handback: Return distilled findings + 1-sentence user summary.
