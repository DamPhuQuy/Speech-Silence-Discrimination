# Evaluation, Benchmarking & Cost Observability Protocol

<observability_and_evals_protocol version="1.0" framework="RIPER-5">

<description>
  Technical standard for monitoring token consumption, model compute budgets,
  execution latency, and quantitative benchmark evaluation frameworks (Evals / Pass@k).
</description>

---

## 1. Trigger-Based Observability & Evals Governance

<trigger_governance>
  To prevent token bloat and eliminate wasted tool calls, the system implements a strict trigger-based activation model:

  ### 1. Default Mode — Lean & Zero-Overhead:
  - **Default is OFF (Zero-Overhead):** For standard routine engineering tasks (CRUD, UI tweaks, bugfixes, docs), the agent MUST NOT consume tool calls or context window measuring tokens, counting intermediate tool calls, or generating benchmark tables. The `<cost_observability>` block in `state.md` remains in its default template values.

  ### 2. Explicit Trigger Mechanisms:
  The agent activates tracking if and only if one of the following triggers is present:
  - **Prompt Flags:**
    - `--profile` or `[profile]`: Activates execution cost and resource monitoring for the task.
    - `--bench` or `[benchmark]`: Activates the quantitative benchmarking lifecycle and creates `results.tsv`.
    - `--eval` or `[eval]`: Activates deterministic governance evaluation fixtures (`process/evals/`).
  - **Task Spec Control Field (`task.md` / `task-lite.md`):**
    - `<observability_mode>PROFILE</observability_mode>`: Activates cost and resource profiling.
    - `<observability_mode>BENCHMARK</observability_mode>`: Activates dual-run A/B benchmarking (baseline vs candidate).

  ### 3. End-of-Task Single-Shot Finalization:
  - When `--profile` is triggered, the agent **MUST NOT** perform repetitive updates to `state.md` after each slice.
  - The agent consolidates metrics (total tool calls, retry count, wall-clock duration) and updates section 14 `<cost_observability>` in `state.md` **exactly once at the end of the EXECUTE phase**, immediately prior to generating `review.md`.

  ### 4. Adaptive Fallback Trigger (Risk-Based):
  The agent automatically activates cost tracking and `<failure_memory>` recording without explicit flags if:
  - A vertical slice fails verification more than once (`retries >= 2`).
  - The task consumes more than 30 tool calls without slice completion.
</trigger_governance>

---

## 2. Cost & Token Observability Governance

<token_cost_governance>
  Every agent session operates under finite token budgets and computational resource limits.

  ### Mandatory Tracked Metrics:
  - **Total Tool Calls:** Number of tool invocations within a task. Raise caution if a task exceeds 50 tool calls without slice completion.
  - **Estimated Input / Output Tokens:** Monitor token consumption to proactively prevent context window bloat.
  - **First-Pass Acceptance Rate:** Track whether slices pass verification on the first attempt or require auto-healing loops.
  - **Wall-Clock Latency:** Total execution time from requirement hydration to Gate 3 sign-off.

  ### Anti-Waste Guardrails:
  1. Never redundantly read unchanged files within the same active session.
  2. Enforce LSP `documentSymbols` or bounded range reading (`offset`/`limit`) for files exceeding 200 lines (with a hard ceiling at 350 lines for any single unconstrained read).
  3. When context consumption hits 60% of window capacity, initiate State Compaction into `state.md` and crystallize verified evidence.
</token_cost_governance>

---

## 3. Git-Atomic Commits & Sandboxing Policy

<atomic_commits_and_sandboxing>
  ### Git-Atomic Commit Convention:
  Upon each vertical slice passing its automated `<verifier>` command with exit code 0, the agent MUST execute an atomic git commit:
  ```bash
  git commit -m "<type>(<task-id>/slice-<index>): <short summary> [verifier: <cmd> (exit: 0)]"
  ```
  *(Example: `git commit -m "feat(CHG-001/slice-01): implement domain entity [verifier: npm test tests/unit.test.ts (exit: 0)]"`)*

  ### Git Worktree Sandboxing Policy:
  - When a subagent executes exploratory research spikes or risky experimental builds, isolate the workspace:
    ```bash
    git worktree add ../scratch-sandbox-<task-id> -b sandbox/<task-id>
    ```
  - After verification is completed and evidence is recorded into `state.md`, cleanly tear down the sandbox:
    ```bash
    git worktree remove ../scratch-sandbox-<task-id> --force
    git branch -D sandbox/<task-id>
    ```
</atomic_commits_and_sandboxing>

---

## 4. Benchmark & Quantitative Evaluation (Evals Framework)

<evals_framework>
  For performance optimization, architectural refactoring, or algorithmic upgrades:

  1. **Baseline Measurement:** Execute benchmark suite before source modifications and record in the `baseline` row of `results.tsv`.
  2. **Post-Innovation Measurement:** Execute identical benchmark in equivalent environment conditions (same CPU/memory, background processes closed).
  3. **Quantitative Gate Criteria:**
     - Reject regressions exceeding 2% throughput degradation or 5% p99 latency increase unless explicitly justified and approved at Gate 1.
</evals_framework>

---

## 5. Deterministic Governance Evals & Evidence Hygiene

<governance_evals>
  Use `process/evals/eval-case.json` as an offline, deterministic fixture. A case records input as data, expected policy verdict, expected side effects, and evidence references; it must never cause a command or MCP call to execute.
  Record only references, hashes, policy verdicts, and verifier exit codes in task artifacts. Never persist secrets, credentials, or raw private tool output.
</governance_evals>

---

## 6. Enterprise Cost Equation Decomposition (Uber Scale Systems Model)

<cost_equation_decomposition>
  To forecast, manage, and curb escalating AI agent expenditures across software factories, session costs are decomposed into six multiplicative terms:

  $$\text{Total Spend} = \text{Users} \times \frac{\text{Requests}}{\text{User}} \times \frac{\text{Turns}}{\text{Request}} \times \frac{\text{Requests}}{\text{Turn}} \times \frac{\text{Tokens}}{\text{Request}} \times \frac{\text{Price}}{\text{Token}}$$

  - **Adoption & Engagement Terms** ($\text{Users}$, $\frac{\text{Requests}}{\text{User}}$): Reflect engineering adoption; encouraged to grow sustainably.
  - **Optimization Target Terms** ($\frac{\text{Turns}}{\text{Request}}$, $\frac{\text{Requests}}{\text{Turn}}$, $\frac{\text{Tokens}}{\text{Request}}$): The primary target for software factory engineering. Eliminating wasted turns, context bloat, and redundant re-reads.
  - **Unit Pricing Term** ($\frac{\text{Price}}{\text{Token}}$): Governed by Pareto-optimal model selection and subagent model tiering.
</cost_equation_decomposition>

---

## 7. The 16 Token Waste Anti-Patterns Matrix (Audit & Optimization Guide)

<token_waste_antipatterns>
  During Phase **REVIEW** or when evaluating `--profile` sessions, audit against these 16 production anti-patterns:

  | # | Anti-Pattern | Root Mechanism | Remediation Protocol |
  |---|---|---|---|
  | **1** | **Suboptimal Model Routing** | Executing simple deterministic tasks or subagent reads on frontier models. | Tier subagents to cost-effective models; reserve frontier models for planning/eval. |
  | **2** | **Persistent Context Bloat** | Storing large raw payloads (e.g. 40KB+ JSON/SQL) across multiple turns. | Code-Mode batching: aggregate and project in subprocess; return summary only. |
  | **3** | **Cache Expiration Inefficiency** | Interactive sessions idling > 5m on short TTL, forcing full-price prefix rebuilds. | Use 1-hour cache TTL for interactive sessions; 5-minute TTL for subagents. |
  | **4** | **Prompt Initialization Overhead** | Loading 100+ MCP schemas upfront (50K–70K tokens) before any prompt is processed. | CLI tool resolution: project tools as shell commands or use dynamic catalog search. |
  | **5** | **Chatty Tool Polling Loops** | Model participating in 3–5 turns of status polling. | Code-Mode: loop internally inside a single Python/Bash script. |
  | **6** | **Unconstrained Bulk Reads** | Ingesting files > 350 lines with `cat` or raw views. | LSP `documentSymbols` outline first, followed by bounded slice reads (< 200 lines). |
  | **7** | **Blind Infinite Retries** | Stacking speculative fixes on broken code without resetting. | LATS Forced Rollback: hard `git checkout` after 2 consecutive failures. |
  | **8** | **Unbounded Test Output Dumps** | Ingesting hundreds of lines of framework bootstrap noise. | Encapsulated Test Runner (`run-test`) with automated stack trace compaction. |
  | **9** | **Semantic Deadlock / Stall** | Modifying identical files with $< 10\%$ diff delta over 3 turns. | Action Trajectory Fingerprinting $\rightarrow$ `STALL_DETECTED` $\rightarrow$ System 2 Root Cause. |
  | **10** | **Drive-by Refactoring** | Formatting untouched code or modifying unapproved files. | Enforce strict negative constraints and `<allowed_files>` scope verifier (`verify-gate`). |
  | **11** | **Excessive Reasoning Output** | Using maximum thinking effort on straightforward coding tasks. | Default reasoning effort to `Medium`, reserving high thinking for R3/R4 complexity. |
  | **12** | **Unprojected Data Fetching** | Requesting wide database tables or unbounded JSON APIs. | Query only required columns / keys (`SELECT id, status` instead of `SELECT *`). |
  | **13** | **Redundant File Ingestion** | Re-reading unchanged source files within the same active turn. | Rely on working memory and LSP symbol navigation. |
  | **14** | **Uncompressed Stack Traces** | Piping full 100-frame framework traces into context. | Retain only failing file, line, and 5 application frames. |
  | **15** | **Stale Task Context Pollution** | Scanning archived completed tasks during current task execution. | Physical filesystem partitioning (`active/` strictly limited to 1 task). |
  | **16** | **Unscoped Wildcard Search** | Grepping across `node_modules/`, `.git/`, or build artifacts. | Strict `.gitignore` alignment and path-scoped regex searches. |
</token_waste_antipatterns>

</observability_and_evals_protocol>
