---
name: mcbs-kill
description: Kill Workers
allowed-tools: Bash
---

# Kill Workers

Terminates one or more Claude workers.

## Commands

### Kill a specific worker
```bash
./claude kill <worker-name>
```

### Kill all workers
```bash
./claude kill-all
# Skip confirmation:
./claude kill-all --force
```

## Before Killing

1. Check active workers:
   ```bash
   ./claude list
   ```

2. Capture output if needed:
   ```bash
   ./claude capture <worker-name> --lines 1000
   ```

3. Update ticket if applicable:
   ```bash
   ./tickets update <ticket-id> --status blocked
   ```

## Use Cases

- **Blocked worker**: No longer responding or in a loop
- **Wrong task**: Incorrect instructions
- **Cleanup**: End of session
- **Error**: Worker in error state

## Notes

- `kill` does not delete associated tickets
- Workers normally terminate with `/exit`
- `kill-all` does NOT kill `prophet-claude`
