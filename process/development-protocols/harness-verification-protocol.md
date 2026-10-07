# Deterministic Test Harness & Log Compactor Protocol

<harness_verification_protocol version="1.0">

<description>
  Standards for deterministic test execution, pre-flight AST syntax verification,
  and log compaction to eliminate context window flooding and Lost-in-the-Middle failures.
</description>

---

## 1. Core Principles

1. **Zero Context Flooding:** Never pipe hundreds of lines of raw terminal output directly into LLM context.
2. **Pre-flight AST Check:** Source changes must pass syntax parsing before launching heavy test suites.
3. **Deterministic Compaction:** The compactor extracts only 3 vital signals upon failure:
   - Failing file path
   - Line number
   - Up to 5 relevant application stack frames (discarding third-party framework plumbing).

---

## 2. Harness Adapter Pipeline

```text
[Source Modification]
       │
       ▼
[Stage 1: AST Syntax Gate] ──(Syntax Error)──► [Fail fast, skip test suite]
       │ (Valid AST)
       ▼
[Stage 2: Linter Auto-fix]  ──► Automatic formatting
       │
       ▼
[Stage 3: Test Execution]   ──► Run validation command
       │
       ▼
[Stage 4: Log Compactor]    ──► Strip framework bootstrap noise
       │
       ▼
[Clean Diagnostic Output to LLM]
```

---

## 3. Standard Execution Command

```bash
# Execute test via built-in adapter:
npx @damphuquy/agent-init run-test -- <command>

# Jest / Vitest example:
npx @damphuquy/agent-init run-test -- npm test -- tests/auth.test.ts

# Pytest example:
npx @damphuquy/agent-init run-test -- pytest tests/test_billing.py
```

---

## 4. Reflex vs. Brain Architecture & System One Gating

1. **Two-Tier Harness Split:**
   - **System One Reflex Layer:** Runs at the pre-flight level with ultra-low latency (70–500ms). Handles: AST syntax verification, automatic linter autofix, smart log compaction, and discrete operation risk classification (R0–R4).
   - **System Two Brain Layer:** Engages frontier generative LLMs only when deep root-cause diagnosis, architectural planning, or complex code implementation is strictly needed.
2. **Confidence-Gated Verification:**
   - When deterministic tests pass and the reflex verification layer confirms zero scope breach or unapproved side-effects with high calibrated confidence, the harness automatically marks the verification step as passed, eliminating wasteful, expensive LLM-as-judge calls.

</harness_verification_protocol>
