# Subagent Delegation & Orchestration Protocol

<orchestration_protocol version="2.0">

<description>
  Engineering guidelines for delegating, isolating, and coordinating subagents during complex, multi-phase tasks. Project-agnostic.
</description>

---

## 1. Delegation Criteria & Workload Triage

<delegation_criteria>
  Subagents should be spawned deliberately for bounded, high-leverage subtasks. Do NOT spawn subagents for trivial steps.

  ### When to Delegate to a Subagent:
  - **Isolated Research Spikes:** Exploring unfamiliar libraries, auditing legacy subsystems, or reading documentation without polluting the parent agent's context window.
  - **Dedicated Quality Audits:** Independent security vulnerability audits, accessibility reviews (a11y), or strict lint/formatting passes.
  - **Orthogonal Test Authoring:** Writing standalone unit test fixtures or integration harnesses for a frozen interface contract.
  - **Parallel Independent Slices:** Implementing non-overlapping, orthogonal components that touch distinct file boundaries.

  ### Fast Reflex Routing Before Delegation (Reflex / System One Pre-routing):
  Before spinning up an expensive System Two Subagent, the Harness or parent agent should evaluate the request with a fast Reflex / System One decision layer to classify intent, estimate complexity, and confirm file boundaries. Avoid spawning heavy subagents for discrete schema lookups or trivial checks that can be resolved instantly.

  ### When Parent Agent MUST Retain Control (Do NOT Delegate):
  - **Architectural Trade-offs & Decisions:** Authoring `decision.md` options and Gate 1 sign-offs.
  - **Master Task Contract & Planning:** Defining `task.md`, vertical slice contracts in `plan.md`, and Gate 2 sign-offs.
  - **Quality Gates & User Approval:** Conducting Gate G3 review sign-off and final `handoff.md` generation.
  - **Interactive User Clarification:** Any prompt requiring direct user guidance or requirement resolution.
</delegation_criteria>

---

## 2. Context Containment & Scoping Rules

<context_containment>
  <rule id="explicit_file_manifest">
    Always provide the subagent with an explicit list of file paths to inspect or modify. Never prompt a subagent with open-ended instructions like "explore the project" or "look around the codebase".
  </rule>

  <rule id="port_and_interface_focus">
    Constrain the subagent's inputs to relevant port interfaces, domain entities, and accompanying test suites. Keep infrastructure noise out of the subagent prompt.
  </rule>

  <rule id="structured_output_contract">
    Always demand a structured output format from the subagent (e.g. unified diff, bulleted findings categorized by Confirmed/Observed/Hypothesized, or JSON/markdown table).
  </rule>
</context_containment>

---

## 3. Concurrency, Isolation & Write Permissions

<concurrency_and_isolation>
  <rule id="zero_write_collision">
    Multiple subagents must NEVER be given write access to the same files or shared mutable database tables concurrently. Overlapping writes cause silent regressions and merge conflicts.
  </rule>

  <rule id="read_only_by_default">
    Default subagents to read-only mode whenever possible (e.g. research, code exploration, audit). Only grant write permissions when the target files are strictly isolated to that subagent.
  </rule>

  <rule id="workspace_isolation">
    If subagents support isolated workspaces (e.g. branch or worktree mode), use them for speculative spike experiments to ensure the parent working tree remains clean.
  </rule>
</concurrency_and_isolation>

---

## 4. State Synchronization & Parent Re-Integration

<state_synchronization>
  <rule id="parent_owns_master_state">
    Subagents must NEVER directly edit the parent's master task artifacts (`task.md`, `state.md`, `review.md`). Only the parent agent reconciles subagent outputs into master state files.
  </rule>

  <rule id="verification_before_acceptance">
    When a subagent returns modified source code or findings, the parent agent must inspect the diff and execute the slice's designated verifier command before accepting the work.
  </rule>

  <rule id="evidence_crystallization">
    Extract verified facts from subagent reports and append them to `state.md > <verification_evidence>`. Discard transient subagent conversation logs to preserve context hygiene.
  </rule>
</state_synchronization>

---

## 5. Reactive Coordination, Timeouts & Failure Recovery

<coordination_and_recovery>
  <rule id="no_polling_loops">
    Never implement sleep-and-poll loops (`while true; sleep 5; check_status`) to monitor subagents. Rely on the system's reactive message wakeup mechanism to resume execution upon subagent completion.
  </rule>

  <rule id="retry_budget_enforcement">
    If a subagent encounters a tool error or recurring failure, enforce the 3-attempt retry budget. If exhausted, record the failure signature in `state.md > <failure_memory>` and escalate to human guidance.
  </rule>

  <rule id="teardown_and_cleanup">
    Terminate idle or failed subagents cleanly. Ensure any temporary scratch files or experiment branches created by the subagent are deleted before completing the slice.
  </rule>
</coordination_and_recovery>

---

## 6. Cross-Harness & Independent Review Protocol

<cross_harness_review>
  <rule id="implementer_cannot_review">
    The subagent or harness that authored an implementation must NEVER act as the sole approver of that slice.
    To prevent confirmation bias, delegate the verification of complex or security-sensitive slices to an independent review subagent, or require human gate sign-off.
  </rule>

  <rule id="adversarial_verification">
    Review subagents must be tasked with finding edge-case regressions, compliance violations, and scope breaches against `<scope_contract>`, rather than merely validating the author's declared success.
  </rule>

  <rule id="fresh_context_mandate">
    Independent review subagents should operate with clean context: they receive the task requirements, the git diff, and the test command, without the conversational baggage or speculative rationale of the implementation loop.
  </rule>
</cross_harness_review>

---

## 7. Multi-Agent Research & Adversarial Topology

<research_topology>
  For complex initiatives (Full Track), the parent agent (Research Coordinator) orchestrates a specialized multi-agent investigation network:

  ```text
                      Research Coordinator
                                │
                ┌───────────────┼───────────────┐
                ↓               ↓               ↓
            Locator         Pattern Miner    Constraint
            Agent              Agent          Analyst
                └───────────────┼───────────────┘
                                ↓
                          Evidence Synthesizer
                                ↓
                          Innovation Agent
                                ↓
                          Adversarial Critic
                                ↓
                               Plan
  ```

  ### Agent Specialization:
  - **Locator Agent:** Explores repository trees, AST, symbols, analyzes call hierarchies (callers/callees), and extracts `file:line` code anchors.
  - **Pattern Miner Agent:** Scans the codebase for existing idioms, conventions, and canonical patterns to guarantee architectural consistency.
  - **Constraint Analyst:** Evaluates concurrency risks, database transaction boundaries, security invariants, and blast radius.
  - **Evidence Synthesizer:** Aggregates findings from parallel investigators, resolves conflicts, classifies the Epistemic Ledger (Confirmed / Observed / Hypothesized), and evaluates the Halting Theorem ($\mathcal{R}_{\text{complete}}$).
  - **Innovation Agent:** Based on verified evidence, drafts 2–3 viable architecture options (A/B/C) with comprehensive trade-off matrices in `decision.md`.
  - **Adversarial Critic (Red Team):** Rigorously stress-tests proposals, uncovering hidden edge cases and regression vulnerabilities before Gate G1 sign-off.

  ### Single-Agent Persona Fallback:
  On runtimes lacking subagent orchestration capabilities or to conserve token budgets, a single agent executes these personas sequentially:
  `Locator` $\rightarrow$ `Pattern Miner` $\rightarrow$ `Constraint Analyst` $\rightarrow$ `Evidence Synthesizer` $\rightarrow$ `Innovation` $\rightarrow$ `Adversarial Critic`.
</research_topology>

---

## 8. Multi-Agent Innovation Topology & Negative Memory Archiving

<innovation_topology>
  During the INNOVATE Phase, following the Evidence Synthesizer output, the system activates a specialized multi-agent pipeline to execute stages I0-I4 and preserve Negative Architectural Memory:

  ```text
                        Evidence Synthesizer
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Design Space Explorer │ (I0)
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   Solution Architect  │ (I1)
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │  Trade-Off Evaluator  │ (I2)
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   Adversarial Critic  │ (I3: Red Team Challenge)
                     └───────────┬───────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │ insufficient evidence         │ verified & challenged
                 ▼                               ▼
        [Backtrack: RESEARCH]        ┌───────────────────────┐
                                     │  Decision Synthesizer │ (I4: Decision & Negative Memory)
                                     └───────────┬───────────┘
                                                 ▼
                                           Gate G1 (I_complete)
  ```

  ### Specialized Roles in INNOVATE:
  - **Design Space Explorer (I0):** Establishes degrees of freedom, identifying mutable dimensions, immutable boundaries, and hard environmental constraints.
  - **Solution Architect (I1):** Synthesizes 2–3 viable candidates (A/B/C) guided by the "Repo-Native First" principle (prioritizing internal patterns, idioms, and existing abstractions over foreign dependencies).
  - **Trade-Off Evaluator (I2):** Assesses options across 7 dimensions: Correctness, Architecture Fit, Complexity, Security, Performance, Migration/Backward Compatibility, and Maintainability.
  - **Adversarial Critic / Red Team (I3):** Interrogates candidates via 4 lethal inquiries: *Why should this design fail under edge conditions? What underlying assumption is invalid? What repository invariant breaks? What did Research miss?* Triggers a backtrack loop (`BACKTRACK_TO_RESEARCH`) if fundamental evidence is absent.
  - **Decision Synthesizer (I4):** Formulates the final recommendation, records residual risks, and **MANDATORILY** archives rejected alternatives into `<rejected_alternatives>` (recording fatal flaws and resurrection conditions). Evaluates the Deterministic Innovation Halting Theorem ($\mathcal{I}_{\text{complete}}$) to clear Gate G1.

  ### Single-Agent Persona Fallback:
  Under single-agent execution or restricted token contexts, the agent adopts these 5 cognitive postures sequentially:
  `Design Space` $\rightarrow$ `Repo-Native Architect` $\rightarrow$ `Trade-Off Analyst` $\rightarrow$ `Adversarial Red Team` $\rightarrow$ `Decision & Negative Memory Registrar`.
</innovation_topology>

</orchestration_protocol>
