# STORY-001a: Implémenter claude-cli

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

As a **développeur solo**
I want to **spawner et gérer des workers Claude dans des sessions tmux**
So that **je puisse déléguer des tâches à des agents isolés sans quitter ma session principale**

---

## Description

### Background
Le claude-cli est le cœur du système Multi-Claude. Il permet de créer des workers Claude dans des sessions tmux isolées, de capturer leur sortie, et de les gérer (lister, tuer). C'est le MVP qui permet de valider le pattern de délégation.

### Fonctionnalités

| Commande | Description |
|----------|-------------|
| `spawn` | Crée un worker Claude dans une nouvelle session tmux |
| `capture` | Capture la sortie d'un worker |
| `list` | Liste les workers actifs |
| `kill` | Termine un worker spécifique |
| `kill-all` | Termine tous les workers |

---

## Scope

### In Scope

- CLI Python avec Click
- Gestion de projet avec uv
- Commandes : spawn, capture, list, kill, kill-all
- Option `--name` pour nommer les sessions
- Option `--role` pour appliquer un rôle (préparation context-cli)
- Auto-exit des workers (envoi /exit)
- README avec documentation

### Out of Scope

- Intégration avec context-cli (STORY-001b)
- Système de tickets (STORY-001c)
- Rôles YAML (juste le flag --role préparé)

---

## User Flow

```
1. Développeur veut déléguer une tâche
   │
   ▼
2. $ claude spawn --name auth-worker "Implémente l'auth JWT"
   │
   ├─► Crée session tmux "auth-worker"
   ├─► Lance claude en mode interactif
   └─► Envoie le prompt via send-keys
   │
   ▼
3. Worker s'exécute de manière autonome
   │
   ▼
4. $ claude capture auth-worker --lines 50
   │
   └─► Affiche les 50 dernières lignes de sortie
   │
   ▼
5. $ claude list
   │
   └─► auth-worker (running, 5min)
   │
   ▼
6. Worker termine avec /exit OU
   $ claude kill auth-worker
```

---

## Acceptance Criteria

### Commande spawn

- [ ] `claude spawn "prompt"` crée une session tmux avec nom auto-généré (claude-XXXXXXXX)
- [ ] `claude spawn --name <name> "prompt"` crée une session avec le nom spécifié
- [ ] `claude spawn --role <role> "prompt"` accepte un flag role (utilisé plus tard)
- [ ] La session lance `claude` en mode interactif
- [ ] Le prompt est envoyé via `tmux send-keys`
- [ ] Un message confirme le spawn avec le nom de session
- [ ] Instructions pour attacher : `tmux attach -t <name>`

### Commande capture

- [ ] `claude capture <session>` affiche les 30 dernières lignes par défaut
- [ ] `claude capture <session> --lines N` affiche N lignes
- [ ] Erreur claire si la session n'existe pas
- [ ] Fonctionne pendant que le worker est actif

### Commande list

- [ ] `claude list` affiche toutes les sessions claude-*
- [ ] Format : nom, état (running), durée
- [ ] Message "No active workers" si aucune session

### Commande kill

- [ ] `claude kill <session>` termine la session spécifiée
- [ ] Confirmation du kill
- [ ] Erreur claire si session inexistante

### Commande kill-all

- [ ] `claude kill-all` termine toutes les sessions claude-*
- [ ] Affiche le nombre de sessions tuées
- [ ] Demande confirmation avant de tuer (--force pour skip)

### Général

- [ ] Projet initialisé avec `uv init`
- [ ] CLI accessible via `uv run python main.py <command>`
- [ ] Wrapper script `claude` pour simplifier l'appel
- [ ] README.md documentant toutes les commandes

---

## Technical Notes

### Structure du Projet

```
bootstrap/claude-cli/
├── pyproject.toml
├── main.py
├── README.md
└── claude              # Wrapper script (optionnel)
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

### Commandes tmux Utilisées

```bash
# Créer session
tmux new-session -d -s <name> "claude"

# Envoyer texte
tmux send-keys -t <name> "text" Enter

# Capturer sortie
tmux capture-pane -t <name> -p

# Lister sessions
tmux list-sessions -F "#{session_name} #{session_created}"

# Tuer session
tmux kill-session -t <name>
```

---

## Dependencies

### Prérequis

- Python 3.11+
- uv installé
- tmux installé
- Claude Code CLI configuré

### Aucune dépendance sur d'autres stories

Cette story est autonome et peut être implémentée en premier.

---

## Definition of Done

- [ ] Projet créé avec `uv init`
- [ ] Les 5 commandes fonctionnent (spawn, capture, list, kill, kill-all)
- [ ] Tests manuels passés :
  - [ ] Spawn un worker, vérifier qu'il apparaît dans tmux
  - [ ] Capture la sortie pendant l'exécution
  - [ ] List affiche le worker
  - [ ] Kill termine le worker
  - [ ] Kill-all termine plusieurs workers
- [ ] README.md documenté
- [ ] Code propre et commenté

---

## Test Plan

### Test 1: Spawn basique
```bash
cd claude-cli
uv run python main.py spawn "Say hello and exit with /exit"
# Vérifier: session créée, message affiché
tmux list-sessions | grep claude-
```

### Test 2: Spawn nommé
```bash
uv run python main.py spawn --name test-worker "Echo TEST"
tmux has-session -t test-worker && echo "OK"
```

### Test 3: Capture
```bash
uv run python main.py capture test-worker --lines 20
# Vérifier: sortie affichée
```

### Test 4: List
```bash
uv run python main.py list
# Vérifier: test-worker listé
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
# Vérifier: "No active workers"
```

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée

---

**Prochaine story:** STORY-001b (context-cli) - Dépend de celle-ci pour le flag --role
