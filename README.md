<div align="center">

![Antigravity to Claude Code](assets/banner.png)

<p align="center">
  <a href="https://x.com/medismera" target="_blank">
    <img src="https://img.shields.io/badge/Author-@medismera-000000?style=for-the-badge&logo=x&logoColor=white" alt="@medismera on X" />
  </a>
</p>

# Antigravity to Claude Code
### Deterministic AST Invariants & Swarm Orchestration Specification

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Target: Google Antigravity](https://img.shields.io/badge/Target-Google%20Antigravity-blue.svg)](#)
[![Specification: Sovereign Invariants](https://img.shields.io/badge/Specification-Sovereign%20Invariants-black.svg)](#)

---

</div>

## Abstract

General-purpose Large Language Models operating in autonomous coding environments degrade due to three systemic defects:
1. **Unbound execution state**: Variable assignment constrained to branching control paths without outer-scope initialization.
2. **Behavioral regressions**: Silent removal of latent invariants during file modifications.
3. **Context dilution**: Unstructured subagent fan-outs polluting the orchestrator's attention budget.

This repository provides the formal software engineering specification and swarm orchestration protocol required to enforce deterministic execution in **Google Antigravity (AGY)**.

---

## 1. Core Invariants (Part I: Code Hygiene)

All code generation and modification routines MUST satisfy these non-negotiable invariants prior to emission:

### INVARIANT 1: Zero-Unbound State
```text
∀ v ∈ OperationalVariables, InScope(v) ⟹ IsInitialized(v, SafeDefault, OuterScope)
```
* Variables MUST NEVER be declared or bound inside conditional blocks (`if`, `switch`, `match`) or exception handlers (`try`, `except`, `catch`) without pre-binding to a typed zero-value default (`None`, `0`, `""`, `[]`, `{}`, `false`, `nil`, `nullptr`) in the outer enclosing scope.
* Every branch assigning an operational variable requires an exhaustive `else` fallback or a preceding early return guard.

### INVARIANT 2: Defensive Traversal
* Nested lookups (`obj.attr`, `map[k]`, `arr[i]`, `ptr->val`) require explicit existence verification or safe-navigation primitives (`.get()`, `?.`, nil guards) prior to dereference.
* Multi-return signatures (`val, err`, `Result<T, E>`) MUST be asserted immediately at the call site.

### INVARIANT 3: Net-Negative Diffs & Three-Line Rule
* Optimization and bug fixes strictly follow the hierarchy: **Delete redundant code > Replace in-place > Add new constructs as a last resort**.
* *The Three-Line Rule*: Three similar lines in-place takes precedence over premature abstraction. Unsolicited helper functions, wrappers, and scaffolding are strictly prohibited.

### INVARIANT 4: Zero Comment Policy
* Baseline comment density is ZERO.
* Comments are permissible ONLY to document non-obvious **WHY** (hardware constraints, memory barriers, upstream protocol bugs).
* Never narrate WHAT code does. Never reference ticket numbers, tasks, or callers.

### INVARIANT 5: Boundary Sanitization & Anti-Masking
* Defensive validation is enforced exclusively at external system boundaries (network I/O, user input, filesystem ingestion).
* Internal boundaries trust system invariants. Silent exception swallowing (`except: pass`) and defensive null fallbacks around internal dependencies are banned. Faults must fail fast.

### INVARIANT 6: Blast Radius & Selective Staging
* Reversible mutations (in-place edits, unit tests) execute freely. Destructive operations (`rm -rf`, `reset --hard`) require confirmation.
* Git staging is strictly selective: `git add <explicit-file-path>`. Indiscriminate operations (`git add .`, `git add -A`) are banned.

### INVARIANT 7: Removed-Behavior Verification
* Prior to deleting or replacing code lines, the invariant or edge-case enforced by those lines must be identified. The refactored state must either preserve that invariant or prove its obsolescence.

### INVARIANT 8: Mandatory Pre-Flight Verification Gate
* Prior to reporting task completion, code must pass silent syntax/compilation validation:
  - Python: `python3 -m py_compile <file>`
  - TypeScript: `tsc --noEmit` / `node --check <file>`
  - Go: `go vet ./...`
  - Rust: `cargo check`

---

## 2. Swarm Governance (Part II: Multi-Agent Orchestration)

Multi-agent coordination in AGY is governed by the following constraints:

### SWARM 1: Non-Delegated Understanding
* The orchestrator MUST NEVER delegate conceptual synthesis. Vague prompts (`"investigate and fix based on findings"`) are prohibited.
* Delegation prompts MUST prove prior understanding: specify exact target paths, line ranges, target AST conditions, and explicit negative constraints.

### SWARM 2: Physical Workspace Isolation
* Subagents performing multi-file modifications MUST execute within an isolated workspace mode (`share` / worktree or `branch`) to guarantee branch isolation and prevent working-tree corruption.

### SWARM 3: Conclusion-Only Handback
* Subagents absorb raw context independently and emit strictly a two-tier handback payload:
  1. **Technical Report**: Exact files, line bounds, compiler exit codes, and commit hashes.
  2. **User Summary**: Exactly ONE sentence relaying the operational outcome.
* Raw file dumps and terminal logs must not cross the subagent boundary.

### SWARM 4: Delegation Restraint
* Tasks touching fewer than 3 files or resolvable within 4 tool calls MUST execute inline within the primary session. Subagents are reserved strictly for decoupled, parallel domains.

---

## 3. Automated Injection & Deployment

### Quick One-Line Automated Injection
Inject the invariants and swarm governance directly into your global Antigravity engine with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/medmera2008-sys/antigravity-to-claude-code/main/install.sh | bash
```

### Targeted Project Workspace Injection
For multi-repo or specific project installations:

```bash
git clone https://github.com/medmera2008-sys/antigravity-to-claude-code.git
cd antigravity-to-claude-code
python3 inject.py --workspace /path/to/project
```

### Injection Topology
The injection engine binds the specification at three deterministic layers:
1. **System Engine Layer**: Native rule injected into `~/.gemini/antigravity-cli/rules/antigravity-to-claude-code.md`.
2. **Global Skill Layer**: Progressive manual injected into `~/.agents/skills/code-constitution/SKILL.md`.
3. **Workspace Layer**: Micro-invariants bound directly into `AGENTS.md`.

---

## 4. International Specifications

<details>
<summary><b>العربية (Arabic Specification Summary)</b></summary>
<br>

### الدستور الصارم لهندسة البرمجيات وحوكمة الأسراب في Google Antigravity

تعمل هذه المنظومة على نقل نماذج الذكاء الاصطناعي من التوليد العشوائي والثرثرة (Vibe Coding) إلى الالتزام الحتمي بشجرة النحو المجردة (AST Invariants):

1. **الصفر-متغيرات مجهولة (`Zero-Unbound State`)**: منع تعريف أي متغير داخل تفرع شرطي دون تهيئة مسبقة بقيمة افتراضية في النطاق الخارجي مع تغطية شاملة لـ `else`.
2. **أفضلية الحذف على الإضافة (`Delete > Replace > Add`)**: إصلاح الأخطاء يجب أن يفضل تقليص الكود وحذف الزوائد على استحداث دوال ومساعدات وهمية.
3. **منع التعمية والفشل السريع (`Anti-Masking & Fail-Fast`)**: حظر استخدام `try/catch` الصامت داخلياً؛ التعقيم يكون فقط عند حدود النظام الخارجية، أما داخلياً يجب الفشل الفوري لكشف العيوب.
4. **عدسة السلوك المحذوف (`Removed-Behavior Auditor`)**: التدقيق في أي سطر كود قبل حذفه لضمان عدم كسر الشروط الحدية السابقة.
5. **حوكمة الأسراب (`Swarm Governance`)**: منع تفويض الفهم العام للوكيل الفرعي (تحديد المسارات والأسطر بدقة)، وإلزامه بإعادة الاستنتاجات فقط دون إغراق السياق بالملفات.

</details>

<details>
<summary><b>한국어 (Korean Specification Summary)</b></summary>
<br>

### Google Antigravity를 위한 결정론적 AST 불변식 및 스웜 거버넌스 사양서

본 명세서는 AI 에이전트의 불확정적 코드 생성(Vibe Coding)을 배제하고 엄격한 소프트웨어 공학 불변식을 강제하기 위한 규격입니다:

1. **비바운드 상태 배제 (`Zero-Unbound State`)**: 외부 스코프에서 기본값 초기화 없이 조건문(`if`, `match`)이나 예외 블록 내에서 변수를 할당하는 행위를 전면 금지합니다.
2. **삭제 우선 원칙 (`Delete > Replace > Add`)**: 버그 수정 시 불필요한 추상화나 헬퍼 함수를 추가하는 대신 기존 코드의 삭제 및 제자리 수정을 최우선합니다.
3. **마스킹 금지 및 조기 실패 (`Anti-Masking & Fail-Fast`)**: 내부 결함을 은폐하는 빈 `try/catch` 블록을 금지하며, 외부 경계 검증 외의 내부 로직은 즉각적으로 실패(`Fail-Fast`)하도록 설계합니다.
4. **삭제된 동작 검증 (`Removed-Behavior Auditor`)**: 코드 삭제 전 해당 라인이 보장하던 기존 불변식을 반드시 검증합니다.
5. **스웜 거버넌스 (`Swarm Governance`)**: 오케스트레이터는 모호한 지시를 하위 에이전트에 위임할 수 없으며, 하위 에이전트는 독립된 작업 트리(`worktree`)에서 실행된 후 결론만 압축 전달해야 합니다.

</details>

---

## 5. Author & License

* **Author**: [@medismera](https://x.com/medismera)
* **License**: [MIT License](LICENSE)
