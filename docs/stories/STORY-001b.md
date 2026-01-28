# STORY-001b: Implémenter context-cli

**Epic:** Multi-Agent Orchestration
**Priority:** Should Have
**Story Points:** 3
**Status:** Not Started
**Assigned To:** Unassigned
**Created:** 2025-01-28
**Sprint:** 1
**Parent:** STORY-001
**Depends On:** STORY-001a

---

## User Story

As a **développeur solo**
I want to **définir des rôles et directives pour mes workers Claude**
So that **chaque worker ait le bon contexte et les bonnes permissions pour sa tâche**

---

## Description

### Background
Le context-cli permet de structurer les contextes Claude de manière modulaire. Au lieu d'un gros CLAUDE.md monolithique, on définit des rôles (prophet-claude, worker, manager) et des directives réutilisables (code-quality, security, etc.). Le CLI génère ensuite le contexte complet et peut produire un settings.json pour les permissions.

### Architecture

```
context-cli/
├── roles/
│   ├── prophet-claude.yaml    # Orchestrateur principal
│   ├── worker.yaml            # Worker générique
│   └── code-reviewer.yaml     # Worker spécialisé
├── directives/
│   ├── base.yaml              # Directives communes
│   ├── code-quality.yaml      # Standards de code
│   └── security.yaml          # Règles de sécurité
└── main.py
```

---

## Scope

### In Scope

- Structure roles/ et directives/ en YAML
- Commande `show <role>` : affiche le contexte combiné
- Commande `list-roles` : liste les rôles disponibles
- Commande `list-directives` : liste les directives
- Commande `settings <role>` : génère settings.json
- Rôles de base : prophet-claude, worker
- Directives de base : base, code-quality

### Out of Scope

- Mémoires persistantes par Claude (future feature)
- Intégration automatique avec claude-cli
- UI pour éditer les rôles

---

## Acceptance Criteria

### Structure YAML

- [ ] Dossier `roles/` créé avec au moins 2 fichiers YAML
- [ ] Dossier `directives/` créé avec au moins 2 fichiers YAML
- [ ] Format rôle : name, description, prompt, directives[]
- [ ] Format directive : name, description, content

### Commande show

- [ ] `context show prophet-claude` affiche le contexte combiné
- [ ] Le prompt du rôle est inclus
- [ ] Les directives listées sont résolues et incluses
- [ ] Erreur claire si rôle inexistant

### Commande list-roles

- [ ] `context list-roles` affiche tous les rôles
- [ ] Format : nom + description courte

### Commande list-directives

- [ ] `context list-directives` affiche toutes les directives
- [ ] Format : nom + description courte

### Commande settings

- [ ] `context settings prophet-claude` génère un JSON valide
- [ ] Le JSON contient les permissions allow/deny
- [ ] Peut être redirigé vers un fichier

### Rôles de base

- [ ] `prophet-claude` : orchestrateur, délègue aux workers
- [ ] `worker` : exécute une tâche spécifique, sort avec /exit

---

## Technical Notes

### Format Rôle YAML

```yaml
# roles/prophet-claude.yaml
name: prophet-claude
description: Main orchestrator Claude, delegates to workers

prompt: |
  You are Prophet Claude, the orchestrator of a multi-Claude system.

  CORE RESPONSIBILITIES:
  - Receive tasks from the human
  - Break down complex tasks
  - Delegate to worker Claudes via claude-cli
  - Monitor worker progress via capture
  - Integrate results

  CONSTRAINTS:
  - NEVER do implementation work yourself
  - NEVER manually kill tmux sessions
  - NEVER block waiting for workers
  - Always delegate non-trivial tasks

directives:
  - base
  - code-quality

permissions:
  allow:
    - "Bash(claude-cli:*)"
    - "Bash(tmux:*)"
    - "Read"
    - "Edit"
  deny:
    - "Bash(rm -rf:*)"
```

### Format Directive YAML

```yaml
# directives/base.yaml
name: base
description: Base directives for all Claudes

content: |
  ## Communication Style
  - Be concise and direct
  - Use code blocks for commands
  - Confirm understanding before acting

  ## Error Handling
  - Report errors clearly
  - Suggest fixes when possible
  - Don't hide failures
```

### main.py - Structure

```python
#!/usr/bin/env python3
"""Context CLI - Manage roles and directives for Claude workers."""

import click
import yaml
import json
from pathlib import Path

ROLES_DIR = Path(__file__).parent / "roles"
DIRECTIVES_DIR = Path(__file__).parent / "directives"

def load_yaml(path: Path) -> dict:
    """Load a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)

def load_role(name: str) -> dict:
    """Load a role by name."""
    path = ROLES_DIR / f"{name}.yaml"
    if not path.exists():
        raise click.ClickException(f"Role not found: {name}")
    return load_yaml(path)

def load_directive(name: str) -> dict:
    """Load a directive by name."""
    path = DIRECTIVES_DIR / f"{name}.yaml"
    if not path.exists():
        raise click.ClickException(f"Directive not found: {name}")
    return load_yaml(path)

@click.group()
def cli():
    """Context CLI - Manage roles and directives."""
    pass

@cli.command()
@click.argument("role_name")
def show(role_name: str):
    """Show combined context for a role."""
    role = load_role(role_name)

    click.echo(f"# Role: {role['name']}")
    click.echo(f"# {role['description']}")
    click.echo()
    click.echo(role['prompt'])
    click.echo()

    # Include directives
    for directive_name in role.get('directives', []):
        directive = load_directive(directive_name)
        click.echo(f"## Directive: {directive['name']}")
        click.echo(directive['content'])
        click.echo()

@cli.command("list-roles")
def list_roles():
    """List available roles."""
    click.echo("Available roles:")
    for path in ROLES_DIR.glob("*.yaml"):
        role = load_yaml(path)
        click.echo(f"  - {role['name']}: {role['description']}")

@cli.command("list-directives")
def list_directives():
    """List available directives."""
    click.echo("Available directives:")
    for path in DIRECTIVES_DIR.glob("*.yaml"):
        directive = load_yaml(path)
        click.echo(f"  - {directive['name']}: {directive['description']}")

@cli.command()
@click.argument("role_name")
def settings(role_name: str):
    """Generate settings.json for a role."""
    role = load_role(role_name)

    permissions = role.get('permissions', {})
    settings = {
        "permissions": {
            "allow": permissions.get('allow', []),
            "deny": permissions.get('deny', [])
        }
    }

    click.echo(json.dumps(settings, indent=2))

if __name__ == "__main__":
    cli()
```

---

## Dependencies

### Prérequis

- Python 3.11+
- uv installé
- PyYAML

### Dépendances Stories

- **STORY-001a** : claude-cli doit exister pour utiliser le flag --role

---

## Definition of Done

- [ ] Projet créé avec `uv init`
- [ ] Structure roles/ et directives/ créée
- [ ] 2 rôles définis : prophet-claude, worker
- [ ] 2 directives définies : base, code-quality
- [ ] 4 commandes fonctionnelles
- [ ] README.md documenté
- [ ] Intégration testée avec claude-cli --role

---

## Test Plan

```bash
cd context-cli

# Test list-roles
uv run python main.py list-roles
# Expected: prophet-claude, worker

# Test list-directives
uv run python main.py list-directives
# Expected: base, code-quality

# Test show
uv run python main.py show worker
# Expected: Combined context output

# Test settings
uv run python main.py settings prophet-claude > settings.json
cat settings.json
# Expected: Valid JSON with permissions
```

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée

---

**Prochaine story:** STORY-001c (tickets-cli)
