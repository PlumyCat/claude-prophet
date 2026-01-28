# STORY-001d: Intégration et Documentation

**Epic:** Multi-Agent Orchestration
**Priority:** Must Have
**Story Points:** 2
**Status:** Not Started
**Assigned To:** Unassigned
**Created:** 2025-01-28
**Sprint:** 1
**Parent:** STORY-001
**Depends On:** STORY-001a, STORY-001b

---

## User Story

As a **développeur solo**
I want to **avoir un système Multi-Claude intégré et documenté**
So that **je puisse démarrer facilement et comprendre comment utiliser le système**

---

## Description

### Background
Cette story finalise le système en intégrant les CLIs ensemble, créant les scripts de démarrage, et documentant le workflow complet. C'est la "glue" qui rend le système utilisable en production.

### Livrables

1. Script `restart-prophet-claude.sh` pour démarrer Prophet Claude
2. Intégration claude-cli + context-cli (flag --role)
3. Wrapper scripts pour simplifier les commandes
4. Documentation complète du workflow
5. CLAUDE.md de base pour Prophet Claude

---

## Scope

### In Scope

- Script de démarrage Prophet Claude
- Intégration --role entre claude-cli et context-cli
- Wrapper scripts (claude, context, tickets)
- README principal avec workflow complet
- CLAUDE.md minimal pour bootstrap
- Exemple de session complète

### Out of Scope

- Installation automatisée (on documente, c'est tout)
- Tests automatisés
- CI/CD

---

## Acceptance Criteria

### Script de démarrage

- [ ] `./restart-prophet-claude.sh` démarre Prophet Claude
- [ ] Applique le contexte du rôle prophet-claude
- [ ] Génère settings.json depuis context-cli
- [ ] Peut être relancé sans problème (idempotent)

### Intégration claude-cli + context-cli

- [ ] `claude spawn --role worker "prompt"` fonctionne
- [ ] Le contexte du rôle est injecté dans le prompt
- [ ] Fonctionne sans --role (comportement par défaut)

### Wrapper scripts

- [ ] `./claude <command>` équivalent à `cd claude-cli && uv run python main.py <command>`
- [ ] `./context <command>` équivalent à `cd context-cli && uv run python main.py <command>`
- [ ] `./tickets <command>` équivalent à `cd tickets-cli && uv run python main.py <command>`
- [ ] Scripts exécutables (chmod +x)

### Documentation

- [ ] README.md principal avec :
  - [ ] Vue d'ensemble du système
  - [ ] Prérequis d'installation
  - [ ] Quick start (5 min)
  - [ ] Workflow complet documenté
  - [ ] Référence des commandes
- [ ] CLAUDE.md minimal pour Prophet Claude

---

## Technical Notes

### Structure Finale

```
bootstrap/
├── README.md                     # Documentation principale
├── CLAUDE.md                     # Contexte Prophet (minimal)
├── restart-prophet-claude.sh     # Script de démarrage
├── claude                        # Wrapper → claude-cli
├── context                       # Wrapper → context-cli
├── tickets                       # Wrapper → tickets-cli
├── claude-cli/
│   └── ...
├── context-cli/
│   └── ...
└── tickets-cli/
    └── ...
```

### restart-prophet-claude.sh

```bash
#!/bin/bash
# Restart Prophet Claude with proper context

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Generating settings.json..."
cd context-cli && uv run python main.py settings prophet-claude > ../settings.json
cd ..

echo "Starting Prophet Claude..."
# Kill existing if any
tmux kill-session -t prophet-claude 2>/dev/null || true

# Start new session
tmux new-session -d -s prophet-claude "claude --settings settings.json"

echo "Prophet Claude started!"
echo "Attach with: tmux attach -t prophet-claude"
```

### Wrapper Scripts

```bash
#!/bin/bash
# claude - wrapper for claude-cli
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/claude-cli"
exec uv run python main.py "$@"
```

### Intégration --role dans claude-cli

```python
# Dans spawn(), ajouter:
if role:
    # Get context from context-cli
    result = subprocess.run(
        ["uv", "run", "python", "../context-cli/main.py", "show", role],
        capture_output=True, text=True, cwd=Path(__file__).parent
    )
    if result.returncode == 0:
        context = result.stdout
        full_prompt = f"{context}\n\n---\n\nTASK:\n{prompt}"
    else:
        click.echo(f"Warning: Could not load role '{role}'", err=True)
        full_prompt = prompt
else:
    full_prompt = prompt
```

### CLAUDE.md Minimal

```markdown
# Prophet Claude

You are Prophet Claude, the orchestrator of a multi-Claude system.

## Quick Reference

- Spawn worker: `./claude spawn --role worker "task"`
- Capture output: `./claude capture <session>`
- List workers: `./claude list`
- Kill worker: `./claude kill <session>`

## Constraints

- NEVER do implementation work - delegate to workers
- NEVER block waiting for workers
- NEVER manually kill tmux sessions

## Context

Full context is managed by context-cli. See `./context show prophet-claude`.
```

### README.md Structure

```markdown
# Multi-Claude Bootstrap System

Orchestrate multiple Claude instances for parallel, asynchronous work.

## Overview

[Diagram ASCII de l'architecture]

## Prerequisites

- Python 3.11+
- uv package manager
- tmux
- Claude Code CLI configured

## Quick Start

1. Clone and setup
2. Start Prophet Claude
3. Delegate your first task

## Workflow

### Basic Delegation
[Exemple complet]

### Using Tickets
[Exemple avec tickets]

## Command Reference

### claude-cli
[Toutes les commandes]

### context-cli
[Toutes les commandes]

### tickets-cli
[Toutes les commandes]

## Troubleshooting

[Problèmes courants]
```

---

## Dependencies

### Prérequis

- STORY-001a (claude-cli) : Obligatoire
- STORY-001b (context-cli) : Obligatoire pour --role
- STORY-001c (tickets-cli) : Optionnel (wrapper script si présent)

---

## Definition of Done

- [ ] `./restart-prophet-claude.sh` fonctionne
- [ ] `./claude spawn --role worker "test"` fonctionne
- [ ] Wrapper scripts créés et exécutables
- [ ] README.md complet
- [ ] CLAUDE.md minimal créé
- [ ] Workflow complet testé de bout en bout

---

## Test Plan

### Test End-to-End

```bash
# 1. Démarrer Prophet Claude
./restart-prophet-claude.sh
tmux attach -t prophet-claude

# 2. Dans Prophet Claude, déléguer une tâche
./claude spawn --role worker --name test-worker "List files in /tmp and exit"

# 3. Vérifier le worker
./claude list
./claude capture test-worker

# 4. Créer un ticket (si tickets-cli présent)
./tickets create "Test task"
./tickets list

# 5. Nettoyer
./claude kill-all --force
```

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée

---

**Fin du Sprint 1** - Système Multi-Claude Bootstrap opérationnel !
