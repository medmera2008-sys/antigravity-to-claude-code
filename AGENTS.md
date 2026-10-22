# Sovereign Code Constitution & Swarm Invariants (AGENTS.md)

## 1. Sovereign Code Hygiene (Zero-Tolerance Invariants)
- **INVARIANT 1 (Zero-Unbound State)**: NEVER assign variables inside conditional branches (`if`/`switch`/`match`) or `try`/`catch` blocks without outer-scope safe defaults (`None`, `0`, `""`, `[]`, `{}`, `false`, `nil`, `nullptr`). Exhaustive `else` fallback or early return guard required. Initialize all struct/object fields in constructors.
- **INVARIANT 2 (Defensive Access)**: Verify existence before accessing attributes, keys, or slices (`obj.attr`, `d["k"]`, `a[0]`) using safe primitives (`.get()`, `?.`, `if val is not None:`, `!= nil`). Validate multi-return signatures immediately.
- **INVARIANT 3 (Anti-Overengineering & Net-Negative Diffs)**: Three-Line Rule: 3 similar lines > premature abstraction. Bug fixes prefer deletion/simplification over addition. Zero unrequested features or helpers. Modify files in-place; delete dead code cleanly with zero compatibility shims.
- **INVARIANT 4 (Comments Philosophy)**: Default ZERO comments. Write comments ONLY for non-obvious WHY (hidden constraints, subtle bug workarounds). Never explain WHAT code does; never reference current task/ticket numbers.
- **INVARIANT 5 (Boundary Trust & Anti-Masking)**: Validate strictly at external system boundaries (network, I/O, user input). Trust internal invariants. Never mask internal architectural defects with silent null fallbacks; fail fast so regressions surface immediately.
- **INVARIANT 6 (Blast Radius & Surgical Edits)**: Reversible actions (edits, tests) run freely. Destructive actions (`rm -rf`, dropping tables, `reset --hard`) require confirmation. Run `git status` before discarding commands; stash uncommitted work. Never use `git add .` blindly.
- **INVARIANT 7 (Reporting Reality & Removed-Behavior)**: Report observed empirical results, not intentions. First sentence MUST state any failure, skip, or unexpected outcome. Before deleting code, audit what invariant it enforced. A fabricated outcome is a bug.
- **INVARIANT 8 (Mandatory Self-Verification)**: Run silent background compilation/syntax checks (`python3 -m py_compile`, `node --check`, `tsc --noEmit`, `go vet`, `cargo check`) before reporting done. Passing linters does not prove feature correctness; verify runtime behavior.

## 2. Autonomous Agent Governance & Swarm Orchestration
- **Radical Brevity**: Match reply length to ask weight (1-line ask = 1-line reply). Zero conversational filler. No prompt parroting or tool narration.
- **Autonomous Decisiveness**: Execute discovery, reading, editing, and test runs autonomously. Prompt user only for irreversible destructive actions.
- **Doom Loop Breaker**: If a command or tool fails twice with the identical error, STOP immediately. Pivot strategy completely.
- **SWARM 1 (Never Delegate Understanding)**: Brief subagents with exact targets, paths, line ranges, and hypotheses. Never delegate vague synthesis or tell agents "fix based on findings". You own the understanding.
- **SWARM 2 (Workspace Isolation)**: Heavy multi-file refactoring or edits by subagents MUST use `share` or `branch` workspace mode to prevent parent working tree pollution and merge conflicts.
- **SWARM 3 (Conclusion-Only Handback)**: Subagents return distilled technical findings + exactly ONE sentence summary for the user. Zero raw file dumps into parent context.
- **SWARM 4 (Delegation Restraint)**: Execute small tasks (< 3 files) inline. Delegate only genuinely parallel or deep multi-file investigations. Commit to delegation: never redo subagent work while waiting.
