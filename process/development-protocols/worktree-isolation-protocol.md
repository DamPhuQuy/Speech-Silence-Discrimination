# Ephemeral Git Worktree Isolation Protocol

<worktree_isolation_protocol version="1.0">

<description>
  Standards for executing agent tasks in isolated Ephemeral Git Worktrees.
  Guarantees zero workspace contamination on developer branches.
</description>

---

## 1. Operational Principles

1. **Isolated Execution:** All modifications, test executions, and atomic slice commits occur exclusively within the worktree sandbox directory.
2. **Atomic Promotion:** Source code is merged/applied to the main branch only after 100% Gate G3 approval.
3. **Clean Teardown:** Upon completion or cancellation, worktrees and temporary branches are purged cleanly.

---

## 2. Ephemeral Sandbox Lifecycle

```text
[Task Init] ──► `git worktree add .agent-worktrees/<task-id> -b agent-sandbox/<task-id>`
       │
       ▼
[RIPER Execution] ──► Edit & test inside worktree directory
       │
       ▼
[Gate G3 100% Pass] ──► Apply diff/merge to developer's main branch
       │
       ▼
[Auto Teardown] ──► `git worktree remove --force .agent-worktrees/<task-id>`
```

---

## 3. Standard Commands

```bash
# Start task inside an isolated sandbox worktree:
npx @damphuquy/agent-init start <task-id> --sandbox

# Promote changes from sandbox back to developer branch:
npx @damphuquy/agent-init apply <task-id>
```

</worktree_isolation_protocol>
