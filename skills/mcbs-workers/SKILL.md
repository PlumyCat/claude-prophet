---
name: mcbs-workers
description: Workers Management
allowed-tools: Bash
---

# Workers Management

Lists and manages active Claude workers.

## Commands

### List active workers
```bash
./claude list
```

### View all tmux sessions
```bash
tmux list-sessions 2>/dev/null || echo "No active tmux sessions"
```

## Output Format

For each worker, display:
- Session name
- Status (running/stopped)
- Activity duration

## Quick Actions

1. Capture output: `/capture <name>`
2. Kill a worker: `/kill <name>`
3. Kill all: `./claude kill-all`
4. New worker: `/spawn`

## Notes

- Claude sessions prefixed with `claude-` unless explicitly named
- Prophet Claude: `prophet-claude` session
