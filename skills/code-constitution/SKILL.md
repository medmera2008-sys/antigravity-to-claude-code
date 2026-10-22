---
name: code-constitution
description: The Sovereign Software Engineering Constitution & Deep Architectural Guide. Use when designing, writing, refactoring, or auditing complex multi-file codebases, performing security reviews, or debugging subtle variable/state initialization bugs across Python, Go, Rust, TypeScript, and C/C++.
---

# The Sovereign Software Engineering Constitution & Deep Architectural Reference

This specification defines the formal, language-agnostic software engineering constitution and deterministic AST invariants required for high-assurance autonomous coding agents.

---

# PART I: Code Generation & AST Invariants

---

## Pillar 1: Zero-Unbound State & Control Flow Completeness

### 1.1 Explicit Initialization Before Branching
* **Invariant**: NEVER declare or assign a variable inside a conditional branch (`if`/`switch`/`match`) or exception block (`try`/`except`/`catch`) without explicitly binding it to a safe default in the outer enclosing scope.
* **Safe Defaults Matrix**:
  - **Python**: `None`, `""`, `0`, `[]`, `{}`, `False`
  - **TypeScript / JavaScript**: `null`, `undefined`, `""`, `0`, `[]`, `{}`, `false`
  - **Go**: explicit zero values (`var buf strings.Builder`, `var count int`, `nil`)
  - **Rust**: `None` (`Option<T>`), explicit default binding
  - **C / C++**: `nullptr`, `0`, explicit zero-initialization (`{0}`)

### 1.2 Exhaustive Branch Coverage
* **Invariant**: If any branch in a conditional block assigns an operational variable, every path MUST explicitly guarantee a valid assigned state via an exhaustive `else` fallback or a preceding early return guard.
* **Anti-Pattern**:
  ```python
  if condition:
      result = compute()
  # If condition is False, result causes UnboundLocalError / NameError
  process(result)
  ```
* **Correct Invariant**:
  ```python
  result = None
  if condition:
      result = compute()
  else:
      result = fallback_value()
  process(result)
  ```

### 1.3 Constructor Initialization Exclusivity
* All object attributes and struct fields must be declared and initialized in constructors (`__init__`, `New()`, constructor).
* Never dynamically inject or attach new attributes to instances inside arbitrary downstream methods.

### 1.4 Safe Traversal & Immediate Validation
* Never access nested properties, keys, or slices (`obj.attr`, `data["key"]`, `arr[0]`, `ptr->val`) without existence verification or safe-navigation primitives (`.get()`, `?.`, `if val is not None:`, nil pointer guards).
* Multi-return signatures (e.g., Go `val, err`, Rust `Result`/`Option`, Python tuples) must be validated immediately at the call site before referencing the payload.

---

## Pillar 2: The Karpathy Invariants & Surgical Execution

Derived from Andrej Karpathy's software development heuristics.

### 2.1 Think Before Coding
* State explicit intent before touching code: identify the root cause, trace the call stack, and determine the exact AST nodes to modify.
* Differentiate between symptoms and causes: never patch an exception symptom at the top level when the defect originated upstream.

### 2.2 The "Delete > Replace > Add" Hierarchy
* **Rule**: When fixing bugs or refactoring, preference strictly follows:
  1. **Delete**: Can the bug be solved by removing redundant logic or dead code?
  2. **Replace**: Can the bug be solved by modifying an existing line or tightening an invariant in-place?
  3. **Add**: Adding new code, helper functions, or abstractions is the last resort and requires explicit justification.
* Bug fixes should aim for net-negative diffs where possible.

### 2.3 Simplicity First & The Three-Line Rule
* Do not introduce abstractions for hypothetical future requirements.
* **The Three-Line Rule**: Three similar lines in-place is far superior to a premature abstraction or unnecessary helper function.

### 2.4 Goal-Driven Empirical Execution
* Verify against actual runtime behavior and compiler outcomes, never speculative belief.
* Run code, execute minimal reproducible scripts, and verify exit codes directly.

---

## Pillar 3: Multi-Angle Regression Auditing

When modifying existing code, apply three specialized audit angles before finalizing any diff.

### 3.1 Angle B: The Removed-Behavior Auditor
* **Rule**: Before deleting or replacing any lines of code, ask:
  > *"What invariant, edge case, or bug workaround were these existing lines protecting?"*
* Confirm that the new implementation either:
  1. Continues to enforce that exact invariant, or
  2. Proves why the invariant is rendered obsolete by architectural changes.
* Never blindly remove checks or guards to make new code fit.

### 3.2 Angle C: Cross-File Caller Tracer
* **Rule**: When changing a function signature, return type, exception behavior, or mutation side-effect, trace **every call site across the entire workspace**.
* Never assume the caller is aware of modified contracts. Check:
  - Argument orders and default parameters.
  - Nil/null handling expectations.
  - Return value destructuring.

### 3.3 Angle E: Re-Entrancy & Shared State Isolation
* When introducing async tasks, callbacks, or proxy wrappers, verify:
  - Are mutable state variables shared across concurrent tasks?
  - Can re-entrant invocations corrupt shared caches or counters?
  - Are resource locks released in `finally` / `defer` blocks?

---

## Pillar 4: Architectural Simplicity & Error Elimination (Ousterhout)

Derived from John Ousterhout (*A Philosophy of Software Design*).

### 4.1 Define Errors Out of Existence
* **Principle**: The best way to handle errors is to design APIs so that there is no error to handle.
* Define operations so that edge cases, empty sets, and out-of-range bounds are natural, valid values rather than exceptional branches:
  - Example: A substring or slice operation on an empty collection should return an empty collection, not throw an out-of-bounds error.
  - Example: A deletion of a non-existent key in an idempotent store is a no-op success, not a fatal exception.

### 4.2 Anti-Masking / Fail-Fast Principle
* **Rule**: NEVER use defensive fallback defaults or silent `try-except: pass` around internal components that MUST exist by architectural design.
* Defensive coding is for **untrusted external boundaries**, not internal plumbing.
* If an internal dependency, config file, or database handler is missing, fail immediately and loudly with a descriptive error. Silent fallbacks mask wiring defects until production.

### 4.3 Mandatory Network & I/O Timeouts
* Every external socket, HTTP call, process invocation, and database query MUST have an explicit, non-zero timeout.
* Unbounded blocking calls cause cascading thread/goroutine exhaustion.

---

## Pillar 5: Comments & Identifiers Philosophy

### 5.1 Default to Zero Comments
* The baseline standard is **ZERO comments**. Write a comment ONLY when the **WHY** cannot be inferred by a senior engineer:
  - A subtle hardware, OS, or protocol quirk.
  - A non-obvious race condition or memory barrier.
  - A workaround for a known upstream bug with an issue link.
* **The Deletion Test**: If deleting the comment would not confuse a competent engineer reading the code, delete it immediately.

### 5.2 Never Explain WHAT Code Does
* Do NOT narrate code mechanics in comments; expressive naming and clean AST structure already communicate what happens.
* NEVER mention ticket numbers, issue IDs, task prompts, or callers in comments (`// fixed issue #42`, `// used by frontend`).

---

## Pillar 6: High-Severity Language Gotchas Checklist

Review this checklist when working across specific languages to prevent silent AST defects:

### 6.1 Go (Golang)
* **Interface Nil Trap**: An interface containing a concrete `nil` pointer is NOT `nil` (`var p *T = nil; var i I = p; i != nil` is true!). Always return an untyped `nil` for error/interface types.
* **Slice Backing Array Mutation**: Slicing an existing slice (`s[a:b]`) shares the underlying backing array; `append` can overwrite sibling slices unless the 3-index slice (`s[a:b:b]`) is used to force reallocation.
* **Leaking Goroutines & Tickers**: Every `time.NewTicker` MUST be stopped (`ticker.Stop()`). Never leave goroutines blocked on unbuffered channels without cancellation contexts.

### 6.2 Python
* **Iterator / Generator Exhaustion**: Generators, `map()`, and `filter()` objects are single-pass iterators. Calling `len()` or iterating once exhausts them; convert to `list()` or `tuple()` if multiple passes are required.
* **Late-Binding Closures in Loops**: Functions created in loops bind variables by reference, not value (`[lambda: i for i in range(5)]` all return 4). Bind early via default arguments: `lambda i=i: i`.
* **Mutable Default Arguments**: Never write `def fn(arg=[]):`. Use `def fn(arg=None): if arg is None: arg = []`.

### 6.3 TypeScript / JavaScript
* **Unchecked Type Assertions (`as T`)**: `as T` tells the compiler to shut up; it performs zero runtime validation. Avoid using `as` to mask potential `undefined` or mismatched API payloads. Use runtime type guards or Zod/valibot schemas.
* **Floating / Unhandled Promises**: Never leave promises floating without `await`, `void`, or `.catch()`. Floating rejections crash Node.js or cause silent task loss.
* **Sparse Arrays & Object De-Optimization**: Avoid `delete obj.key` in hot loops as it alters V8 hidden classes (Shapes); set `obj.key = undefined` instead.

### 6.4 Rust
* **Unnecessary Cloning**: Avoid `.clone()` as a quick fix to satisfy the borrow checker. Use references (`&T`), slices (`&str`, `&[T]`), or `Cow<'a, T>` unless owned values are strictly necessary.
* **Deadlocks on Mutex Poisoning**: Always anticipate lock poisoning when handling panics across threads.

---

## Pillar 7: Epistemic Honesty & Three-State Verification

### 7.1 Three-State Verification Phase
When verifying changes, outcomes must be categorized into one of three distinct states:
1. **`PASS`**: Empirically verified via compiler check, test execution, or browser inspection with zero errors.
2. **`FAIL_WITH_ROOT_CAUSE`**: Failed with a concrete stack trace or log pointing to the identified defect.
3. **`INCONCLUSIVE`**: Cannot run or verify due to missing external dependencies or headless environment. State this plainly: *"I did not test this empirically because X."*

### 7.2 Failures Lead the First Sentence
* If any step failed, was skipped, or yielded unexpected output, state it plainly in the **very first sentence** of the response.
* Never conceal errors behind optimistic summaries. A visible issue is fixable; a concealed failure is catastrophic.

### 7.3 Mandatory Silent Pre-Flight Syntax Check
Before reporting any code task complete, execute silent syntax verification:
* **Python**: `python3 -m py_compile <file>`
* **Node/TS**: `node --check <file>` or `tsc --noEmit`
* **Go**: `go vet ./...` or `go build -v`
* **Rust**: `cargo check`

---

# PART II: Subagent Orchestration & Swarm Governance

Formal multi-agent coordination protocol, workspace isolation calculus, and execution invariants.

---

## Pillar 8: The Principle of Non-Delegated Understanding

The single most frequent cause of subagent failure and hallucinated code is abdication of understanding by the orchestrator.

### 8.1 "Never Delegate Understanding"
* **Rule**: NEVER write prompts like:
  - *"Based on your research, fix the bug."*
  - *"Investigate the issue and implement whatever is needed."*
  - *"Explore the codebase and make it work."*
* Those phrases push synthesis onto the subagent rather than doing it yourself.
* **The Sovereign Briefing Invariant**:
  Write prompts that prove YOU understood the root cause. A compliant delegation prompt MUST include:
  1. The exact file path(s) and specific line ranges (`file.py#L45-L60`).
  2. The specific hypothesis or AST condition being modified.
  3. The explicit constraints (e.g., "Do not alter signature X; ensure return type Y").
  4. The required output format and length cap.

### 8.2 Prescribe Questions for Investigations, Exact Commands for Lookups
* **Lookups**: Hand over the exact shell command or search pattern (`grep -rn "pattern"`).
* **Investigations**: Hand over the specific question, not prescribed intermediate steps (prescribed steps become dead weight when the initial premise is wrong).

---

## Pillar 9: Delegation Restraint & The Three-File Gate

Subagents multiply latency and token consumption. Each subagent establishes a fresh context, re-explores, and reports back, which the orchestrator must then digest.

### 9.1 The Three-File Threshold
* **Inline by Default**: If a subtask involves reading/editing fewer than 3 files or can be completed in under 4 tool calls, do it **inline in the primary session**.
* Do NOT spawn a subagent for single-fact lookups, quick edits, or minor test runs.

### 9.2 Commitment to Delegation
* Once a task is delegated to a subagent, **commit to the delegation**:
  - Do NOT redo the subagent's work while waiting.
  - Do NOT launch duplicate searches in the parent session.
  - Do NOT re-derive the findings once reported. If you find yourself doing what the subagent is doing, the subagent should never have been spawned.

### 9.3 Low Spawn Counts & Independent Tracks
* Parallel subagents are exclusively for **genuinely independent, non-overlapping tracks** (e.g., examining two completely decoupled modules).
* Never fan out multiple subagents on a single modest problem. One well-briefed agent is worth ten loosely-briefed ones.

---

## Pillar 10: Physical Workspace Isolation (Git Worktree / AGY Workspace Modes)

Concurrent file modifications on the same directory cause race conditions, dirty working trees, and merge conflicts.

### 10.1 Workspace Mode Calculus
When invoking subagents via `invoke_subagent`, choose the workspace mode deliberately:
* **`inherit`** (Default): Use ONLY for read-only investigations, web research, or documentation lookups where no files will be written.
* **`share`**: Creates a shared workspace attached to the underlying repository directory (an isolated worktree from the parent tree). Use for independent branch operations and multi-file code modifications without duplicating heavy disk storage.
* **`branch`**: Creates a fully isolated workspace cloned/branched from the parent. Use for destructive testing, experimental refactors, or multi-step migrations where failures must not leak into the parent tree.

### 10.2 Subagent Write Boundary Guard
* Any subagent modifying files must commit its changes atomically on its designated branch before completing.
* Never permit a subagent to run destructive un-stashed commands (`git reset --hard`, `git clean -fd`) on a shared working tree.

---

## Pillar 11: Structured Handback & Context Hygiene

Subagents must never pollute the parent orchestrator's context window with bulky terminal logs, raw file dumps, or conversational filler.

### 11.1 Conclusion-Only Reporting ("Keep the Conclusion, Not the Dumps")
* Subagents absorb thousands of lines of code during exploration, but they MUST return only the distilled synthesis to the orchestrator.
* Raw file contents, 100-line diffs, and verbose linter output must remain in the subagent's local log; only the conclusion crosses the boundary.

### 11.2 The Two-Tier Handback Schema
Every subagent report to the orchestrator MUST adhere to this two-tier format:
```markdown
### 1. Technical Report (For Orchestrator / Caller)
- Exact files modified / investigated with line numbers.
- Invariants verified and test results (`PASS` / `FAIL_WITH_ROOT_CAUSE`).
- Commit hash or patch summary (e.g., `committed 7a8b9c`).

### 2. User Summary (One Sentence Relay)
- Exactly ONE concise sentence that the orchestrator can relay directly to the human user without re-synthesis.
```

### 11.3 Atomic Termination
* Delivery of the final report marks the end of the subagent's lifecycle.
* Any conversational pleasantries, open-ended questions, or trailing chat generated after the report are ignored by the harness.

---

## Pillar 12: Swarm Concurrency & Git Staging Discipline

### 12.1 Selective Staging Invariant
* Subagents and orchestrators MUST ONLY stage files intentionally created or modified for the assigned task.
* **STRICT PROHIBITION**: NEVER use `git add .` or `git add -A`. Always stage specific explicit paths:
  ```bash
  git add path/to/file1.py path/to/file2.ts
  ```

### 12.2 Scope Containment
* Workers must complete exactly what was asked. If a worker discovers an unrelated bug or architectural flaw during execution, it must NOT fix it silently; it reports it as a separate follow-up candidate in its technical report.
