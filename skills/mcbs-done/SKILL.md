---
name: mcbs-done
description: Done - Task Completion
allowed-tools: Bash
---

# Done - Task Completion

Signals the completion of a task assigned to a worker.

## Usage

This skill is intended for **workers** to signal that they have completed their task.

## Actions to Perform

### 1. Ask for ticket ID (if not known)

### 2. Update the ticket
```bash
./tickets update <ticket-id> --status done
./tickets comment <ticket-id> "Task completed by worker"
```

### 3. Remind /exit

IMPORTANT: Always remind the worker to do `/exit` to free the tmux session.

## Workflow

```
Worker completes its task
       │
       ▼
   /done <ticket-id>
       │
       ├─► tickets update → done
       ├─► tickets comment → "Completed"
       │
       ▼
   Reminder: /exit
       │
       ▼
   Worker does /exit
       │
       ▼
   Tmux session freed
```

## Notes

- This skill does NOT do `/exit` automatically
- If no ticket, just remind to do `/exit`
