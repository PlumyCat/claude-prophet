---
name: mcbs-capture
description: Capture Worker Output
allowed-tools: Bash
---

# Capture Worker Output

Captures and displays output from a Claude worker.

## Commands

### Capture last lines (default: 50)
```bash
./claude capture <worker-name>
```

### Capture more lines
```bash
./claude capture <worker-name> --lines 100
```

### Capture entire buffer
```bash
./claude capture <worker-name> --lines 5000
```

## Before Capturing

Verify the worker exists:
```bash
./claude list
```

## Interpretation

Look for in the output:
- **Errors**: Error messages or exceptions
- **Progress**: Progress indicators
- **Completion**: Task completion messages
- **/exit**: Worker terminated properly

## Next Actions

- **In progress**: Wait and recapture later
- **Blocked**: Analyze, kill and respawn
- **Completed**: Retrieve result, update ticket
- **Error**: Diagnose and relaunch
