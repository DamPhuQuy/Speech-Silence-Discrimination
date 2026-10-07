# Code-Mode Tool Batching & Subprocess Execution Protocol

<code_mode_protocol version="1.0">

<description>
  Standards for batching multi-step tool calls, polling loops, and data aggregation
  into single-turn executable scripts (Code-Mode) to prevent context bloat, eliminate
  wasteful turns, and slash token consumption by 50% to 99%.
</description>

---

## 1. Core Motivation & Uber Scale Findings

Empirical research from Uber's Software Factory demonstrates that interacting with chatty tools (databases, cloud status polling, multi-page REST APIs, SaaS integrations) via standard multi-turn LLM tool-use introduces severe context overhead:

* **The Problem:** In standard LLM tool-use, every individual action requires a complete model round-trip. For a simple SQL query or status check, the model participates in a polling loop (2 to 5 turns), re-transmitting the entire session history and loading massive raw intermediate payloads into the active context window.
* **The Code-Mode Solution:** Instead of participating in the loop across multiple conversational turns, the agent authors a targeted execution script (Python, Node.js, or Bash) that runs in a subprocess. The loop, error retries, and data aggregation execute entirely in the subshell, and **only the final aggregated summary is emitted back to the model context**.
* **Empirical Token Savings:**
  * Simple queries (`SELECT 1`, `COUNT(*)`): **55% – 58% token savings**.
  * Aggregations (`GROUP BY LIMIT 20`, schema lookups): **71% token savings**.
  * Large result sets / wide tables: **> 90% – 99% token savings**.

---

## 2. When to Use Code-Mode vs. Standard Tool Calls

| Operational Characteristic | Standard Single Tool Call | Code-Mode Batching (Recommended) |
|---|---|---|
| **Action Count** | Exactly 1 discrete action (e.g. read 1 file). | $\ge 2$ sequential or dependent actions. |
| **Execution Pattern** | Instantaneous single-shot return. | Polling loop, wait-until-ready, retry-on-status. |
| **Data Payload Volume** | Small, bounded snippet (< 100 lines). | Large raw payload requiring filtering, sorting, or projection. |
| **API Protocol Style** | Simple deterministic RPC. | Chatty protocol (e.g., query -> job_id -> poll -> fetch rows). |
| **Context Impact** | Minimal (< 300 tokens). | High risk of flooding context with megabytes of JSON/SQL logs. |

---

## 3. The 4 Golden Rules of Code-Mode Batching

1. **Keep Intermediate Polling in Subprocess:**
   Never output raw polling heartbeats or retry counters to stdout. The script must loop internally (with reasonable timeout and backoff) and only write the final exit state.
2. **Aggregate & Project Before Returning to Context:**
   Never dump hundreds of uninspected rows or unbounded JSON objects to stdout. The script must parse, slice, and project only the minimal fields required by the task:
   ```bash
   # WRONG: Dumping 5,000 raw JSON objects into LLM context:
   curl -s https://api.internal/service/endpoints

   # RIGHT: Filtering in subshell, returning only target subset:
   python3 -c "import json, urllib.request; data = json.load(urllib.request.urlopen('https://api.internal/service/endpoints')); print([x['id'] for x in data if x['status'] == 'FAILED'])"
   ```
3. **Deterministic Error Signatures:**
   If the batch script encounters an unexpected condition, it must exit with a non-zero exit code (`exit 1`) and print a concise 1-line error signature to stderr so the agent can diagnose without context pollution.
4. **Clean Ephemeral Scratch Space:**
   Store temporary scripts in a dedicated scratch directory (`/tmp/` or designated task scratchpad). Delete or clean scratch scripts once the verified result is committed.

---

## 4. Canonical Implementation Patterns

### Pattern A: Asynchronous Job Polling Loop
```python
# python3 scratch/poll_job.py
import time, sys, requests

job_id = sys.argv[1]
max_retries = 30
for attempt in range(max_retries):
    res = requests.get(f"http://localhost:8080/api/jobs/{job_id}").json()
    if res["status"] == "COMPLETED":
        print(f"SUCCESS: Job {job_id} completed in {res['duration_ms']}ms. Summary: {res['summary']}")
        sys.exit(0)
    elif res["status"] in ("FAILED", "CANCELLED"):
        print(f"FAILED: Job {job_id} failed with error: {res.get('error')}", file=sys.stderr)
        sys.exit(1)
    time.sleep(2)

print("TIMEOUT: Job polling exceeded 60s limit", file=sys.stderr)
sys.exit(2)
```

### Pattern B: Database Batch Inspection & Schema Verification
```bash
# Querying multiple tables and checking constraints in a single turn:
python3 -c "
import sqlite3, json
conn = sqlite3.connect('local.db')
cursor = conn.cursor()
tables = ['users', 'billing_accounts', 'subscriptions']
report = {}
for t in tables:
    cursor.execute(f'PRAGMA table_info({t});')
    report[t] = [row[1] for row in cursor.fetchall()]
print(json.dumps(report, indent=2))
"
```

---

## 5. Verification & Review Integration

During Phase **REVIEW** (Gate G3), inspect all tool-use traces:
* Verify that no raw, unaggregated datasets persist in artifact memory (`state.md`).
* Flag any multi-turn chatty polling loop as an optimization papercut and consider encapsulating into a reusable CLI script or repository utility.

</code_mode_protocol>
