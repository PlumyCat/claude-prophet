# Multi-Claude Bootstrap System - Usage Guide

> Complete documentation for the multi-agent Claude orchestration system

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Key Concepts](#key-concepts)
6. [Workflows](#workflows)
7. [Command Reference](#command-reference)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

### What is the Multi-Claude Bootstrap?

A system for orchestrating **multiple Claude instances** working in parallel. A main Claude ("Prophet Claude") delegates tasks to isolated workers in tmux sessions.

### Why use this system?

| Problem | Solution |
|---------|----------|
| Complex tasks = saturated context | Delegate to specialized workers |
| Sequential work = slow | Asynchronous parallel workers |
| Context lost on restart | Persistent roles and directives |
| No task tracking | Integrated ticket system |

### Use Cases

- **Parallel development**: One worker on backend, one on frontend
- **Code review**: Specialized worker with review directives
- **Massive refactoring**: Multiple workers on different modules
- **Documentation**: Dedicated worker for doc generation

---

## Architecture

### Global Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         HUMAN                                   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   PROPHET CLAUDE                        │    │
│  │                   (Orchestrator)                        │    │
│  │                                                         │    │
│  │  • Receives human requests                              │    │
│  │  • Breaks down into sub-tasks                           │    │
│  │  • Delegates to workers                                 │    │
│  │  • Supervises and integrates                            │    │
│  │                                                         │    │
│  │  Tools: claude-cli, context-cli, tickets-cli            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                     │
│            ┌──────────────┼──────────────┐                      │
│            │              │              │                      │
│            ▼              ▼              ▼                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │   WORKER 1   │ │   WORKER 2   │ │   WORKER N   │             │
│  │   (tmux)     │ │   (tmux)     │ │   (tmux)     │             │
│  │              │ │              │ │              │             │
│  │ • Specific   │ │ • Specific   │ │ • Specific   │             │
│  │   task       │ │   task       │ │   task       │             │
│  │ • Isolated   │ │ • Isolated   │ │ • Isolated   │             │
│  │   context    │ │   context    │ │   context    │             │
│  │ • Auto-exit  │ │ • Auto-exit  │ │ • Auto-exit  │             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Components

```
bootstrap/
│
├── claude-cli/          # Tmux worker management
│   ├── spawn            # Create a worker
│   ├── capture          # View output
│   ├── list             # List workers
│   └── kill             # Terminate a worker
│
├── context-cli/         # Context management
│   ├── roles/           # Role definitions
│   ├── directives/      # Reusable rules
│   ├── show             # Display a context
│   └── settings         # Generate settings.json
│
├── tickets-cli/         # Task tracking
│   ├── tickets/         # JSON storage
│   ├── create           # Create a ticket
│   ├── assign           # Assign a worker
│   └── update           # Change status
│
└── scripts/
    └── restart-prophet-claude.sh
```

### Data Flow

```
                    ┌─────────────┐
                    │ context-cli │
                    │             │
                    │ roles/      │
                    │ directives/ │
                    └──────┬──────┘
                           │
                           │ generates context
                           ▼
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│ tickets-cli │◄────│ claude-cli  │────►│    tmux     │
│             │     │             │     │             │
│ • tracking  │     │ • spawn     │     │ • sessions  │
│ • states    │     │ • capture   │     │ • isolation │
│ • history   │     │ • kill      │     │ • send-keys │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Installation

### Prerequisites

```bash
# Python 3.11+
python3 --version  # >= 3.11

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# tmux
sudo apt install tmux  # Ubuntu/Debian
brew install tmux      # macOS

# Claude Code CLI
# Must be installed and configured with an active account
claude --version
```

### System Installation

```bash
# Clone or create the folder
mkdir -p ~/workspace/bootstrap
cd ~/workspace/bootstrap

# Initialize claude-cli
mkdir claude-cli && cd claude-cli
uv init
uv add click
# ... copy main.py

# Initialize context-cli
cd .. && mkdir context-cli && cd context-cli
uv init
uv add click pyyaml
# ... copy main.py and create roles/, directives/

# Initialize tickets-cli (optional)
cd .. && mkdir tickets-cli && cd tickets-cli
uv init
uv add click
# ... copy main.py

# Create wrapper scripts
cd ..
# ... create claude, context, tickets scripts
chmod +x claude context tickets restart-prophet-claude.sh
```

---

## Quick Start

### 1. Start Prophet Claude

```bash
cd ~/workspace/bootstrap
./restart-prophet-claude.sh

# Or manually:
tmux new-session -d -s prophet-claude "claude"
tmux attach -t prophet-claude
```

### 2. Delegate your first task

In Prophet Claude:

```bash
# Spawn a worker
./claude spawn --name hello-worker "Say 'Hello World' and then exit with /exit"

# Check that it's running
./claude list

# View its output
./claude capture hello-worker

# Clean up
./claude kill hello-worker
```

### 3. Use roles

```bash
# View available roles
./context list-roles

# Spawn with a role
./claude spawn --role worker --name code-worker "Implement a fibonacci function in Python"

# The worker receives the "worker" role context
```

---

## Key Concepts

### Prophet Claude vs Workers

| Aspect | Prophet Claude | Worker Claude |
|--------|----------------|---------------|
| **Role** | Orchestrator | Executor |
| **Lifespan** | Permanent | Temporary |
| **Context** | Complete (system) | Specialized (task) |
| **Actions** | Delegate, supervise | Implement, report |
| **Tmux session** | `prophet-claude` | `claude-XXXXXXXX` |

### Tmux Sessions

```
┌─────────────────────────────────────────────────────┐
│ tmux server                                         │
│                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐   │
│  │ prophet-claude      │  │ claude-abc12345     │   │
│  │ (attached)          │  │ (detached)          │   │
│  │                     │  │                     │   │
│  │ Human ◄──► Claude   │  │ Worker Claude       │   │
│  │                     │  │ (autonomous)        │   │
│  └─────────────────────┘  └─────────────────────┘   │
│                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐   │
│  │ claude-def67890     │  │ claude-ghi11111     │   │
│  │ (detached)          │  │ (detached)          │   │
│  └─────────────────────┘  └─────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Roles and Directives

```yaml
# Role structure
roles/worker.yaml:
  name: worker
  description: "Worker for delegated tasks"
  prompt: |
    You are a Worker Claude. Complete the task and exit.

    CONSTRAINTS:
    - Focus on the given task
    - Don't start new tasks
    - Exit with /exit when done

  directives:
    - base           # Includes directives/base.yaml
    - code-quality   # Includes directives/code-quality.yaml

# Directive structure
directives/code-quality.yaml:
  name: code-quality
  description: "Code quality standards"
  content: |
    ## Code Standards
    - Tests for each function
    - Descriptive names
    - No dead code
```

### Ticket System

```
┌─────────────────────────────────────────────────────────┐
│                    TICKET LIFECYCLE                     │
│                                                         │
│   ┌──────┐    ┌─────────────┐    ┌─────────┐    ┌────┐  │
│   │ OPEN │───►│IN-PROGRESS  │───►│ BLOCKED │───►│DONE│  │
│   └──────┘    └─────────────┘    └─────────┘    └────┘  │
│       │              │                 │           ▲    │
│       │              │                 │           │    │
│       └──────────────┴─────────────────┴───────────┘    │
│                                                         │
│   create          assign            update       update │
│                   (auto)                                │
└─────────────────────────────────────────────────────────┘
```

---

## Workflows

### Basic Workflow: Simple Delegation

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Human requests a complex task                       │
│     │                                                   │
│     ▼                                                   │
│  2. Prophet Claude analyzes and decomposes              │
│     │                                                   │
│     ├─────────────────────────────────────────┐         │
│     ▼                                         ▼         │
│  3. ./claude spawn "Sub-task 1"    ./claude spawn "Sub-task 2"
│     │                                         │         │
│     ▼                                         ▼         │
│  4. Worker 1 executes              Worker 2 executes    │
│     │                                         │         │
│     ▼                                         ▼         │
│  5. ./claude capture worker1    ./claude capture worker2│
│     │                                         │         │
│     └─────────────────┬───────────────────────┘         │
│                       ▼                                 │
│  6. Prophet Claude integrates results                   │
│     │                                                   │
│     ▼                                                   │
│  7. Human receives complete deliverable                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Advanced Workflow: With Tickets

```bash
# Prophet Claude receives: "Add JWT authentication"

# 1. Create the ticket
./tickets create "Implement JWT Auth" --body "Backend + Frontend"

# 2. Spawn and assign
./claude spawn --role worker --name auth-backend "Implement JWT backend"
./tickets assign <ticket-id> auth-backend

# 3. Supervise
./claude capture auth-backend --lines 50
./tickets show <ticket-id>

# 4. When complete
./tickets update <ticket-id> --status done
```

### Workflow: Code Review

```bash
# Define a reviewer role
# context-cli/roles/code-reviewer.yaml

# Spawn the reviewer
./claude spawn --role code-reviewer --name reviewer-pr123 \
  "Review the changes in src/auth.py for security issues"

# Capture the report
./claude capture reviewer-pr123 > review-report.md
```

---

## Command Reference

### claude-cli

| Command | Description | Example |
|---------|-------------|---------|
| `spawn` | Create a worker | `./claude spawn "task"` |
| `spawn --name` | Named worker | `./claude spawn --name my-worker "task"` |
| `spawn --role` | With a role | `./claude spawn --role worker "task"` |
| `capture` | View output | `./claude capture my-worker` |
| `capture --lines` | Last N lines | `./claude capture my-worker --lines 100` |
| `list` | List workers | `./claude list` |
| `kill` | Kill a worker | `./claude kill my-worker` |
| `kill-all` | Kill all | `./claude kill-all --force` |

### context-cli

| Command | Description | Example |
|---------|-------------|---------|
| `show` | Display context | `./context show worker` |
| `list-roles` | List roles | `./context list-roles` |
| `list-directives` | List directives | `./context list-directives` |
| `settings` | Generate settings.json | `./context settings prophet-claude` |

### tickets-cli

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create a ticket | `./tickets create "Title"` |
| `create --body` | With description | `./tickets create "Title" --body "Details"` |
| `create --assign` | Create + assign | `./tickets create "Title" --assign worker` |
| `list` | List tickets | `./tickets list` |
| `list --status` | Filter by status | `./tickets list --status open` |
| `list --assigned` | Filter by worker | `./tickets list --assigned my-worker` |
| `show` | Ticket details | `./tickets show abc123` |
| `assign` | Assign a worker | `./tickets assign abc123 my-worker` |
| `update --status` | Change status | `./tickets update abc123 --status done` |
| `comment` | Add a comment | `./tickets comment abc123 "Progress update"` |
| `delete` | Delete a ticket | `./tickets delete abc123 --force` |
| `stats` | Global statistics | `./tickets stats` |

---

## Best Practices

### For Prophet Claude

```
✅ DO:
- Delegate non-trivial tasks
- Give clear instructions to workers
- Check regularly with capture
- Use descriptive session names

❌ DON'T:
- Do implementation work
- Wait for a worker to finish (non-blocking)
- Manually kill tmux sessions
- Attach to worker sessions
```

### For Workers

```
✅ DO:
- Focus on the assigned task
- Exit with /exit when done
- Report blockers clearly

❌ DON'T:
- Start new unasked tasks
- Modify files out of scope
- Stay active after completion
```

### Session Naming

```
Good:
- auth-backend-worker
- feature-42-implementation
- code-review-pr-123

Bad:
- worker1
- test
- claude-session
```

---

## Troubleshooting

### "Session not found"

```bash
# Check existing sessions
tmux list-sessions

# The worker may have finished (auto-exit)
# Relaunch if needed
./claude spawn --name <name> "task"
```

### "No active workers"

```bash
# Normal if all have finished with /exit
# Check tmux history
tmux list-sessions -a
```

### Stuck worker

```bash
# Capture to see the state
./claude capture <worker> --lines 100

# If really stuck, kill and respawn
./claude kill <worker>
./claude spawn --name <worker> "corrected task"
```

### Context not applied

```bash
# Check that the role exists
./context list-roles

# Check the role content
./context show <role>

# Regenerate settings.json if needed
./context settings <role> > settings.json
```

---

## Appendices

### Useful tmux Commands

```bash
# List sessions
tmux list-sessions

# Attach to a session (debug only)
tmux attach -t <session>

# Detach (Ctrl+B then D)

# Capture manually
tmux capture-pane -t <session> -p

# Send a command
tmux send-keys -t <session> "command" Enter
```

### Complete Session Example

```bash
# Terminal 1: Prophet Claude
./restart-prophet-claude.sh
tmux attach -t prophet-claude

# In Prophet Claude:
> Implement a Redis cache system for the API

# Prophet responds and delegates:
./claude spawn --role worker --name cache-impl \
  "Implement Redis caching in src/api/cache.py:
   - Connection pool
   - get/set methods
   - TTL support
   - Error handling"

./claude spawn --role worker --name cache-tests \
  "Write tests for Redis cache in tests/test_cache.py"

# Prophet checks:
./claude list
# cache-impl (running)
# cache-tests (running)

./claude capture cache-impl --lines 30
# ... see progress ...

# When done:
./claude capture cache-impl > /tmp/cache-impl-result.md
./claude capture cache-tests > /tmp/cache-tests-result.md

# Integrate and continue
```

---

*Documentation generated from the Multi-Claude Bootstrap tutorial by @claudecodeonly*
*Last updated: 2025-01-28*
