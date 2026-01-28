# STORY-001c: Implémenter tickets-cli

**Epic:** Multi-Agent Orchestration
**Priority:** Could Have
**Story Points:** 3
**Status:** Completed
**Assigned To:** Unassigned
**Created:** 2025-01-28
**Sprint:** 1
**Parent:** STORY-001
**Depends On:** STORY-001a

---

## User Story

As a **développeur solo**
I want to **tracker les tâches déléguées aux workers via un système de tickets**
So that **je puisse suivre l'avancement et coordonner le travail asynchrone**

---

## Description

### Background
Le tickets-cli permet de gérer les tâches de manière asynchrone. Quand Prophet Claude délègue une tâche, il crée un ticket. Le worker est assigné au ticket et met à jour son état. Cela permet de tracker le travail en cours, les blocages, et l'historique.

### Workflow

```
Prophet                          Worker
   │                                │
   ├─► tickets create "Auth JWT"    │
   │   └─► Ticket #abc123 created   │
   │                                │
   ├─► tickets assign abc123 auth-worker
   │                                │
   ├─► claude spawn --name auth-worker "..."
   │                                │
   │                                ├─► (travaille...)
   │                                │
   ├─► tickets show abc123          │
   │   └─► Status: in-progress      │
   │                                │
   │                                ├─► tickets update abc123 --status done
   │                                │
   └─► tickets list                 │
       └─► abc123: done ✓           │
```

---

## Scope

### In Scope

- CRUD tickets (create, list, show, update)
- Assignation de workers
- États : open, in-progress, blocked, done
- Stockage JSON simple (un fichier par ticket)
- Historique des changements d'état

### Out of Scope

- Notifications/pings entre Claudes
- Abonnements aux tickets
- ACK system
- Base de données (on reste sur des fichiers JSON)

---

## Acceptance Criteria

### Commande create

- [ ] `tickets create "Title"` crée un ticket avec ID auto-généré
- [ ] `tickets create "Title" --body "Description"` ajoute une description
- [ ] Retourne l'ID du ticket créé
- [ ] État initial : open

### Commande list

- [ ] `tickets list` affiche tous les tickets
- [ ] Format : ID, titre, état, assigné à
- [ ] `tickets list --status open` filtre par état
- [ ] Affiche "No tickets" si vide

### Commande show

- [ ] `tickets show <id>` affiche le détail complet
- [ ] Inclut : titre, description, état, assigné, historique
- [ ] Erreur claire si ticket inexistant

### Commande update

- [ ] `tickets update <id> --status <status>` change l'état
- [ ] États valides : open, in-progress, blocked, done
- [ ] Ajoute une entrée à l'historique
- [ ] Erreur si état invalide

### Commande assign

- [ ] `tickets assign <id> <worker>` assigne un worker
- [ ] Met à jour le champ "assigned_to"
- [ ] Passe automatiquement en "in-progress" si état était "open"

### Stockage

- [ ] Dossier `tickets/` créé automatiquement
- [ ] Un fichier JSON par ticket : `tickets/<id>.json`
- [ ] Format lisible et éditable manuellement

---

## Technical Notes

### Structure du Projet

```
bootstrap/tickets-cli/
├── pyproject.toml
├── main.py
├── README.md
└── tickets/              # Créé automatiquement
    ├── abc123.json
    └── def456.json
```

### Format Ticket JSON

```json
{
  "id": "abc123",
  "title": "Implement JWT authentication",
  "body": "Create login/logout/refresh endpoints with JWT tokens",
  "status": "in-progress",
  "assigned_to": "auth-worker",
  "created_at": "2025-01-28T15:30:00Z",
  "updated_at": "2025-01-28T16:45:00Z",
  "history": [
    {
      "timestamp": "2025-01-28T15:30:00Z",
      "action": "created",
      "details": "Ticket created"
    },
    {
      "timestamp": "2025-01-28T15:35:00Z",
      "action": "assigned",
      "details": "Assigned to auth-worker"
    },
    {
      "timestamp": "2025-01-28T15:35:00Z",
      "action": "status_change",
      "from": "open",
      "to": "in-progress"
    }
  ]
}
```

### main.py - Structure

```python
#!/usr/bin/env python3
"""Tickets CLI - Track delegated tasks."""

import click
import json
import uuid
from pathlib import Path
from datetime import datetime

TICKETS_DIR = Path(__file__).parent / "tickets"

def ensure_tickets_dir():
    TICKETS_DIR.mkdir(exist_ok=True)

def generate_ticket_id() -> str:
    return uuid.uuid4().hex[:8]

def load_ticket(ticket_id: str) -> dict:
    path = TICKETS_DIR / f"{ticket_id}.json"
    if not path.exists():
        raise click.ClickException(f"Ticket not found: {ticket_id}")
    with open(path) as f:
        return json.load(f)

def save_ticket(ticket: dict):
    path = TICKETS_DIR / f"{ticket['id']}.json"
    with open(path, 'w') as f:
        json.dump(ticket, f, indent=2)

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

@click.group()
def cli():
    """Tickets CLI - Track delegated tasks."""
    ensure_tickets_dir()

@cli.command()
@click.argument("title")
@click.option("--body", "-b", default="", help="Ticket description")
def create(title: str, body: str):
    """Create a new ticket."""
    ticket = {
        "id": generate_ticket_id(),
        "title": title,
        "body": body,
        "status": "open",
        "assigned_to": None,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "history": [
            {"timestamp": now_iso(), "action": "created", "details": "Ticket created"}
        ]
    }
    save_ticket(ticket)
    click.echo(f"Created ticket: {ticket['id']}")
    click.echo(f"  Title: {title}")

@cli.command("list")
@click.option("--status", "-s", default=None, help="Filter by status")
def list_tickets(status: str):
    """List all tickets."""
    tickets = []
    for path in TICKETS_DIR.glob("*.json"):
        with open(path) as f:
            ticket = json.load(f)
            if status is None or ticket['status'] == status:
                tickets.append(ticket)

    if not tickets:
        click.echo("No tickets")
        return

    for t in tickets:
        assigned = t['assigned_to'] or 'unassigned'
        status_icon = "✓" if t['status'] == 'done' else "○"
        click.echo(f"{status_icon} {t['id']}: {t['title']} [{t['status']}] → {assigned}")

@cli.command()
@click.argument("ticket_id")
def show(ticket_id: str):
    """Show ticket details."""
    ticket = load_ticket(ticket_id)

    click.echo(f"# {ticket['title']}")
    click.echo(f"ID: {ticket['id']}")
    click.echo(f"Status: {ticket['status']}")
    click.echo(f"Assigned: {ticket['assigned_to'] or 'unassigned'}")
    click.echo(f"Created: {ticket['created_at']}")
    click.echo()

    if ticket['body']:
        click.echo("## Description")
        click.echo(ticket['body'])
        click.echo()

    click.echo("## History")
    for entry in ticket['history']:
        click.echo(f"  - {entry['timestamp']}: {entry['action']}")

@cli.command()
@click.argument("ticket_id")
@click.option("--status", "-s", type=click.Choice(['open', 'in-progress', 'blocked', 'done']))
def update(ticket_id: str, status: str):
    """Update ticket status."""
    ticket = load_ticket(ticket_id)
    old_status = ticket['status']

    ticket['status'] = status
    ticket['updated_at'] = now_iso()
    ticket['history'].append({
        "timestamp": now_iso(),
        "action": "status_change",
        "from": old_status,
        "to": status
    })

    save_ticket(ticket)
    click.echo(f"Updated {ticket_id}: {old_status} → {status}")

@cli.command()
@click.argument("ticket_id")
@click.argument("worker")
def assign(ticket_id: str, worker: str):
    """Assign a worker to a ticket."""
    ticket = load_ticket(ticket_id)

    ticket['assigned_to'] = worker
    ticket['updated_at'] = now_iso()
    ticket['history'].append({
        "timestamp": now_iso(),
        "action": "assigned",
        "details": f"Assigned to {worker}"
    })

    # Auto-transition to in-progress
    if ticket['status'] == 'open':
        ticket['status'] = 'in-progress'
        ticket['history'].append({
            "timestamp": now_iso(),
            "action": "status_change",
            "from": "open",
            "to": "in-progress"
        })

    save_ticket(ticket)
    click.echo(f"Assigned {ticket_id} to {worker}")

if __name__ == "__main__":
    cli()
```

---

## Dependencies

### Prérequis

- Python 3.11+
- uv installé

### Dépendances Stories

- **STORY-001a** : claude-cli pour spawner les workers assignés

---

## Definition of Done

- [ ] Projet créé avec `uv init`
- [ ] 5 commandes fonctionnelles (create, list, show, update, assign)
- [ ] Stockage JSON dans tickets/
- [ ] Historique des changements tracké
- [ ] README.md documenté
- [ ] Tests manuels passés

---

## Test Plan

```bash
cd tickets-cli

# Create
uv run python main.py create "Implement auth" --body "JWT tokens"
# Note the ID returned

# List
uv run python main.py list

# Show
uv run python main.py show <id>

# Assign
uv run python main.py assign <id> auth-worker

# Update
uv run python main.py update <id> --status done

# List filtered
uv run python main.py list --status done
```

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée

---

**Prochaine story:** STORY-001d (Intégration)
