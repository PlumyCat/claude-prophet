---
name: mcbs-prophet
description: Prophet Claude Management
allowed-tools: Bash
---

# Prophet Claude Management

Manages (re)starting Prophet Claude in a dedicated tmux session.

## Launch/Relaunch Prophet Claude

```bash
./restart-prophet-claude.sh
```

The absolute path allows launching from any folder.

This script:
1. Generates `settings.json` from context-cli with the prophet-claude role
2. Kills the old tmux session if it exists
3. Starts a new `prophet-claude` session with Claude
4. Sends the initialization prompt

## Useful Commands

```bash
# Check if Prophet Claude is running
tmux has-session -t prophet-claude 2>/dev/null && echo "Running" || echo "Not running"

# Attach to the session
tmux attach -t prophet-claude

# View state without attaching
tmux capture-pane -t prophet-claude -p | tail -20

# Kill the session
tmux kill-session -t prophet-claude
```

## Architecture

```
You (normal terminal)
  └── claude -c (this conversation = Prophet)
        ├── /spawn worker-1 → tmux session
        ├── /spawn worker-2 → tmux session
        └── /spawn worker-3 → tmux session
```

Prophet Claude can also run in tmux for long autonomous sessions.
