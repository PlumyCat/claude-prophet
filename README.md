# Claude Prophet - Multi-Claude Bootstrap System

Multi-agent Claude orchestration system enabling task delegation to isolated workers in tmux sessions.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                     HUMAN                           │
│                       │                             │
│                       ▼                             │
│  ┌─────────────────────────────────────────────┐    │
│  │             PROPHET CLAUDE                  │    │
│  │            (Orchestrator)                   │    │
│  │                                             │    │
│  │  • Receives requests                        │    │
│  │  • Delegates to workers                     │    │
│  │  • Supervises and integrates                │    │
│  └─────────────────────────────────────────────┘    │
│                       │                             │
│          ┌────────────┼────────────┐                │
│          ▼            ▼            ▼                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │  WORKER 1  │ │  WORKER 2  │ │  WORKER N  │       │
│  │   (tmux)   │ │   (tmux)   │ │   (tmux)   │       │
│  └────────────┘ └────────────┘ └────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- tmux
- Claude Code CLI configured

### Setup

```bash
git clone https://github.com/PlumyCat/claude-prophet.git
cd claude-prophet

# Install dependencies for each CLI
cd claude-cli && uv sync && cd ..
cd context-cli && uv sync && cd ..
cd tickets-cli && uv sync && cd ..

# Install Claude Code skills (MCBS)
./install-skills.sh
```

## Quick Start

```bash
# 1. Start Prophet Claude
./restart-prophet-claude.sh

# 2. Attach to the session
tmux attach -t prophet-claude

# 3. In Prophet Claude, delegate a task
./claude spawn --role worker --name my-task "Implement a fibonacci function"

# 4. Check the worker
./claude list
./claude capture my-task
```

## Components

### claude-cli

Tmux worker management.

```bash
./claude spawn "prompt"              # Spawn a worker
./claude spawn --name foo "prompt"   # With a name
./claude spawn --role worker "prompt" # With a role
./claude capture foo --lines 50      # View output
./claude list                        # List workers
./claude kill foo                    # Kill a worker
./claude kill-all                    # Kill all workers
```

### context-cli

Role and directive management.

```bash
./context list-roles        # List roles
./context list-directives   # List directives
./context show worker       # Display role context
./context settings worker   # Generate settings.json
./context validate worker   # Validate a role
```

### tickets-cli

Delegated task tracking.

```bash
./tickets create "Task"      # Create a ticket
./tickets list               # List tickets
./tickets show abc123        # View a ticket
./tickets assign abc123 worker # Assign a worker
./tickets update abc123 --status done # Mark as done
./tickets stats              # Statistics
```

## Structure

```
claude-prophet/
├── claude                    # Wrapper → claude-cli
├── context                   # Wrapper → context-cli
├── tickets                   # Wrapper → tickets-cli
├── restart-prophet-claude.sh # Startup script
├── install-skills.sh         # Installs MCBS skills
├── claude-cli/               # Worker management CLI
├── context-cli/              # Context management CLI
│   ├── roles/                # Role definitions
│   └── directives/           # Reusable directives
├── tickets-cli/              # Task tracking CLI
│   └── tickets/              # JSON ticket storage
├── skills/mcbs/              # Claude Code skills (MCBS)
│   ├── prophet/              # Prophet Claude management
│   ├── spawn/                # Spawn a worker
│   ├── workers/              # List workers
│   ├── capture/              # Capture output
│   ├── kill/                 # Kill workers
│   ├── status/               # System status
│   ├── ticket/               # Ticket management
│   └── done/                 # Signal task completion
└── docs/
    ├── GUIDE.md              # Complete usage guide
    └── stories/              # User stories
```

## Claude Code Skills (MCBS)

Global skills available from any project (`~/.claude/skills/mcbs/`).

| Skill | Description |
|-------|-------------|
| `/mcbs:prophet` | (Re)launch Prophet Claude in tmux |
| `/mcbs:spawn` | Create a worker with options |
| `/mcbs:workers` | List active workers |
| `/mcbs:capture` | View worker output |
| `/mcbs:kill` | Kill one/all workers |
| `/mcbs:status` | System overview |
| `/mcbs:ticket` | Ticket management |
| `/mcbs:done` | Signal task completion (workers) |

### Usage Example

```bash
# From any terminal with Claude Code
claude

# In Claude
> /mcbs:status           # View system status
> /mcbs:spawn            # Create a worker (interactive)
> /mcbs:workers          # List workers
> /mcbs:capture worker-1 # View output
```

## Documentation

- [Complete Usage Guide](docs/GUIDE.md)
- [claude-cli README](claude-cli/README.md)
- [context-cli README](context-cli/README.md)
- [tickets-cli README](tickets-cli/README.md)

## How This Project Was Created

This project was automatically generated from a 6-hour Twitch video using a "Video-to-Code" pipeline:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Twitch Video   │────▶│ Frame           │────▶│ Frame Analysis  │
│  (6h, no audio) │     │ Extraction      │     │ (GPT-4 Vision)  │
│                 │     │ (ffmpeg)        │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Code    │◀────│ BMAD Stories    │◀────│ Tutorial MD     │
│  Implementation │     │ (User Stories)  │     │ (documentation) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Steps

1. **Download**: `yt-dlp` to fetch the Twitch video
2. **Frame extraction**: `ffmpeg -vf "fps=1/5"` → 4344 frames
3. **Vision analysis**: Azure OpenAI GPT-4.1-mini analyzes frames
4. **Tutorial generation**: Structured Markdown documentation
5. **BMAD Stories**: Conversion to User Stories with BMAD workflow
6. **Implementation**: Claude Code implements each story

### Result

A 6-hour video transformed into a functional system with:
- 3 CLIs (claude-cli, context-cli, tickets-cli)
- 8 Claude Code skills
- Complete multi-agent architecture

## Credits

Based on the Multi-Claude Bootstrap tutorial by [@claudecodeonly](https://www.twitch.tv/claudecodeonly).

A big thank you for this 6-hour Twitch video presenting a truly innovative multi-agent orchestration system. The approach with Prophet Claude, tmux workers, and the ticket system is elegant and powerful.

Source video: https://www.twitch.tv/claudecodeonly/video/2657952550

## License

MIT
