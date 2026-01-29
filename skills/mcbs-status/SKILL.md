---
name: mcbs-status
description: System Status
allowed-tools: Bash
---

# System Status

Overview of the Multi-Claude Bootstrap system.

## Commands to Execute

### 1. Prophet Claude Status
```bash
tmux has-session -t prophet-claude 2>/dev/null && echo "Prophet Claude: RUNNING" || echo "Prophet Claude: STOPPED"
```

### 2. Active Workers
```bash
./claude list
```

### 3. In-Progress Tickets
```bash
./tickets list --status in-progress
./tickets list --status blocked
```

### 4. Ticket Statistics
```bash
./tickets stats
```

### 5. Workers Waiting for Response
```bash
echo "=== Workers waiting ==="
ls ./signals/waiting/*.json 2>/dev/null || echo "No workers waiting"
```

```bash
# Details of waiting tickets
./tickets list --status waiting
```

```bash
# View signal details (if present)
for f in ./signals/waiting/*.json; do
  [ -f "$f" ] && echo "--- $(basename $f .json) ---" && cat "$f"
done 2>/dev/null
```

## Output Format

```
=== Multi-Claude System Status ===

Prophet Claude: [RUNNING/STOPPED]

Active workers: X
  - worker-1 (running)
  - worker-2 (running)

Workers waiting: X
  ⏳ claude-auth: "OAuth or JWT?" (ticket abc123)

Tickets:
  ○ Open: X
  ◐ In-progress: X
  ✗ Blocked: X
  ⏳ Waiting: X
  ✓ Done: X

Tmux sessions: X total
```

## Recommended Actions

- Prophet STOPPED → `/prophet`
- Tickets BLOCKED → Investigate
- Tickets WAITING → `/mcbs:respond <session> "response"`
- No workers but tickets in-progress → Check `/capture`
