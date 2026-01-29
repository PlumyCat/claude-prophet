# STORY-001a: Implement claude-cli

**Epic:** Multi-Agent Orchestration
**Priority:** Must Have
**Story Points:** 5
**Status:** Not Started
**Assigned To:** Unassigned
**Created:** 2025-01-28
**Sprint:** 1
**Parent:** STORY-001

---

## User Story

As a **solo developer**
I want to **spawn and manage Claude workers in tmux sessions**
So that **I can delegate tasks to isolated agents without leaving my main session**

---

## Description

### Background
The claude-cli is the core of the Multi-Claude system. It allows creating Claude workers in isolated tmux sessions, capturing their output, and managing them (list, kill). This is the MVP that validates the delegation pattern.

### Features

| Command | Description |
|---------|-------------|
| `spawn` | Creates a Claude worker in a new tmux session |
| `capture` | Captures a worker's output |
| `list` | Lists active workers |
| `kill` | Terminates a specific worker |
| `kill-all` | Terminates all workers |

---

## Scope

### In Scope

- Python CLI with Click
- Project management with uv
- Commands: spawn, capture, list, kill, kill-all
- `--name` option to name sessions
- `--role` option to apply a role (preparation for context-cli)
- Worker auto-exit (send /exit)
- README with documentation

### Out of Scope

- Integration with context-cli (STORY-001b)
- Ticket system (STORY-001c)
- YAML roles (just the --role flag prepared)

---

## User Flow

```
1. Developer wants to delegate a task
   │
   ▼
2. $ claude spawn --name auth-worker "Implement JWT auth"
   │
   ├─► Creates tmux session "auth-worker"
   ├─► Launches claude in interactive mode
   └─► Sends the prompt via send-keys
   │
   ▼
3. Worker executes autonomously
   │
   ▼
4. $ claude capture auth-worker --lines 50
   │
   └─► Displays the last 50 lines of output
   │
   ▼
5. $ claude list
   │
   └─► auth-worker (running, 5min)
   │
   ▼
6. Worker terminates with /exit OR
   $ claude kill auth-worker
```

---

## Acceptance Criteria

### spawn command

- [ ] `claude spawn "prompt"` creates a tmux session with auto-generated name (claude-XXXXXXXX)
- [ ] `claude spawn --name <name> "prompt"` creates a session with the specified name
- [ ] `claude spawn --role <role> "prompt"` accepts a role flag (used later)
- [ ] The session launches `claude` in interactive mode
- [ ] The prompt is sent via `tmux send-keys`
- [ ] A message confirms the spawn with the session name
- [ ] Instructions to attach: `tmux attach -t <name>`

### capture command

- [ ] `claude capture <session>` displays the last 30 lines by default
- [ ] `claude capture <session> --lines N` displays N lines
- [ ] Clear error if session doesn't exist
- [ ] Works while the worker is active

### list command

- [ ] `claude list` displays all claude-* sessions
- [ ] Format: name, state (running), duration
- [ ] "No active workers" message if no sessions

### kill command

- [ ] `claude kill <session>` terminates the specified session
- [ ] Confirmation of the kill
- [ ] Clear error if session doesn't exist

### kill-all command

- [ ] `claude kill-all` terminates all claude-* sessions
- [ ] Displays the number of sessions killed
- [ ] Asks for confirmation before killing (--force to skip)

### General

- [ ] Project initialized with `uv init`
- [ ] CLI accessible via `uv run python main.py <command>`
- [ ] Wrapper script `claude` to simplify the call
- [ ] README.md documenting all commands

---

## Technical Notes

### Project Structure

```
bootstrap/claude-cli/
├── pyproject.toml
├── main.py
├── README.md
└── claude              # Wrapper script (optional)
```

### pyproject.toml

```toml
[project]
name = "claude-cli"
version = "0.1.0"
description = "CLI to spawn and manage Claude workers in tmux"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
]

[project.scripts]
claude-cli = "main:cli"
```

### main.py - Structure

```python
#!/usr/bin/env python3
"""Claude CLI - Spawn and manage Claude workers in tmux sessions."""

import click
import subprocess
import uuid
from datetime import datetime

def run_tmux(*args) -> subprocess.CompletedProcess:
    """Execute a tmux command."""
    return subprocess.run(["tmux", *args], capture_output=True, text=True)

def generate_session_name() -> str:
    """Generate unique session name."""
    return f"claude-{uuid.uuid4().hex[:8]}"

@click.group()
def cli():
    """Claude CLI - Spawn and manage Claude workers in tmux."""
    pass

@cli.command()
@click.argument("prompt")
@click.option("--name", "-n", default=None, help="Session name")
@click.option("--role", "-r", default=None, help="Role to apply (requires context-cli)")
def spawn(prompt: str, name: str, role: str):
    """Spawn a Claude worker in a new tmux session."""
    session = name or generate_session_name()

    # Create tmux session with claude
    run_tmux("new-session", "-d", "-s", session, "claude")

    # Wait for claude to start
    import time
    time.sleep(2)

    # Send the prompt
    run_tmux("send-keys", "-t", session, prompt, "Enter")

    click.echo(f"Spawned worker: {session}")
    click.echo(f"Attach with: tmux attach -t {session}")

@cli.command()
@click.argument("session")
@click.option("--lines", "-l", default=30, help="Number of lines to capture")
def capture(session: str, lines: int):
    """Capture output from a worker session."""
    result = run_tmux("capture-pane", "-t", session, "-p")
    if result.returncode != 0:
        click.echo(f"Error: Session '{session}' not found", err=True)
        return

    output_lines = result.stdout.strip().split("\n")
    for line in output_lines[-lines:]:
        click.echo(line)

@cli.command("list")
def list_sessions():
    """List active Claude worker sessions."""
    result = run_tmux("list-sessions", "-F", "#{session_name} #{session_created}")
    if result.returncode != 0:
        click.echo("No active workers")
        return

    sessions = [s for s in result.stdout.strip().split("\n") if s.startswith("claude-")]
    if not sessions:
        click.echo("No active workers")
        return

    click.echo("Active workers:")
    for session in sessions:
        click.echo(f"  - {session}")

@cli.command()
@click.argument("session")
def kill(session: str):
    """Kill a specific worker session."""
    result = run_tmux("kill-session", "-t", session)
    if result.returncode != 0:
        click.echo(f"Error: Session '{session}' not found", err=True)
        return
    click.echo(f"Killed: {session}")

@cli.command("kill-all")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def kill_all(force: bool):
    """Kill all Claude worker sessions."""
    result = run_tmux("list-sessions", "-F", "#{session_name}")
    if result.returncode != 0:
        click.echo("No sessions to kill")
        return

    sessions = [s for s in result.stdout.strip().split("\n") if s.startswith("claude-")]
    if not sessions:
        click.echo("No Claude sessions to kill")
        return

    if not force:
        click.confirm(f"Kill {len(sessions)} session(s)?", abort=True)

    for session in sessions:
        run_tmux("kill-session", "-t", session)

    click.echo(f"Killed {len(sessions)} session(s)")

if __name__ == "__main__":
    cli()
```

### tmux Commands Used

```bash
# Create session
tmux new-session -d -s <name> "claude"

# Send text
tmux send-keys -t <name> "text" Enter

# Capture output
tmux capture-pane -t <name> -p

# List sessions
tmux list-sessions -F "#{session_name} #{session_created}"

# Kill session
tmux kill-session -t <name>
```

---

## Dependencies

### Prerequisites

- Python 3.11+
- uv installed
- tmux installed
- Claude Code CLI configured

### No dependencies on other stories

This story is standalone and can be implemented first.

---

## Definition of Done

- [ ] Project created with `uv init`
- [ ] All 5 commands work (spawn, capture, list, kill, kill-all)
- [ ] Manual tests passed:
  - [ ] Spawn a worker, verify it appears in tmux
  - [ ] Capture output during execution
  - [ ] List displays the worker
  - [ ] Kill terminates the worker
  - [ ] Kill-all terminates multiple workers
- [ ] README.md documented
- [ ] Clean and commented code

---

## Test Plan

### Test 1: Basic spawn
```bash
cd claude-cli
uv run python main.py spawn "Say hello and exit with /exit"
# Verify: session created, message displayed
tmux list-sessions | grep claude-
```

### Test 2: Named spawn
```bash
uv run python main.py spawn --name test-worker "Echo TEST"
tmux has-session -t test-worker && echo "OK"
```

### Test 3: Capture
```bash
uv run python main.py capture test-worker --lines 20
# Verify: output displayed
```

### Test 4: List
```bash
uv run python main.py list
# Verify: test-worker listed
```

### Test 5: Kill
```bash
uv run python main.py kill test-worker
tmux has-session -t test-worker 2>/dev/null || echo "Killed OK"
```

### Test 6: Kill-all
```bash
uv run python main.py spawn "Test 1"
uv run python main.py spawn "Test 2"
uv run python main.py kill-all --force
uv run python main.py list
# Verify: "No active workers"
```

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story created

---

**Next story:** STORY-001b (context-cli) - Depends on this one for the --role flag
