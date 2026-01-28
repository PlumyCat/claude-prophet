# tickets-cli

CLI pour tracker les tâches déléguées aux workers Claude.

## Installation

```bash
cd tickets-cli
uv sync
```

## Concept

```
Prophet Claude                          Worker Claude
      │                                       │
      ├─► tickets create "Auth JWT"           │
      │   └─► Ticket #abc123 created          │
      │                                       │
      ├─► tickets assign abc123 auth-worker   │
      │                                       │
      ├─► claude spawn --name auth-worker ... │
      │                                       │
      │                                       ├─► (travaille...)
      │                                       │
      ├─► tickets show abc123                 │
      │   └─► Status: in-progress             │
      │                                       │
      │                                       ├─► tickets update abc123 --status done
      │                                       │
      └─► tickets list                        │
          └─► abc123: done ✓                  │
```

## Commandes

### create

Crée un nouveau ticket.

```bash
# Basique
uv run python main.py create "Implement JWT auth"

# Avec description
uv run python main.py create "Fix login" --body "Users can't login with email"

# Avec assignation immédiate
uv run python main.py create "Add tests" --assign test-worker
```

### list

Liste les tickets.

```bash
# Tous les tickets
uv run python main.py list

# Filtrer par status
uv run python main.py list --status open
uv run python main.py list --status in-progress

# Filtrer par worker
uv run python main.py list --assigned auth-worker
```

### show

Affiche les détails d'un ticket.

```bash
uv run python main.py show abc123

# Supporte les IDs partiels
uv run python main.py show abc
```

### update

Met à jour un ticket.

```bash
# Changer le status
uv run python main.py update abc123 --status done
uv run python main.py update abc123 --status blocked

# Mettre à jour la description
uv run python main.py update abc123 --body "New description"

# Changer le titre
uv run python main.py update abc123 --title "New title"
```

### assign

Assigne un worker à un ticket.

```bash
uv run python main.py assign abc123 auth-worker
```

Note: Si le ticket est "open", il passe automatiquement en "in-progress".

### comment

Ajoute un commentaire à un ticket.

```bash
uv run python main.py comment abc123 "Started implementation, 50% done"
```

### delete

Supprime un ticket.

```bash
uv run python main.py delete abc123

# Sans confirmation
uv run python main.py delete abc123 --force
```

### stats

Affiche les statistiques.

```bash
uv run python main.py stats
```

## États

| État | Icône | Description |
|------|-------|-------------|
| open | ○ | Nouveau ticket, pas encore assigné |
| in-progress | ◐ | En cours de traitement |
| blocked | ✗ | Bloqué (attente d'info, dépendance) |
| done | ✓ | Terminé |

## Stockage

Les tickets sont stockés en JSON dans `tickets/`:

```
tickets-cli/
└── tickets/
    ├── abc12345.json
    └── def67890.json
```

Format d'un ticket:

```json
{
  "id": "abc12345",
  "title": "Implement JWT authentication",
  "body": "Create login/logout endpoints",
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
    }
  ]
}
```

## Intégration avec claude-cli

Workflow typique:

```bash
# 1. Prophet crée un ticket
./tickets create "Implement feature X" --body "Details..."

# 2. Prophet assigne et spawn le worker
./tickets assign abc123 feature-worker
./claude spawn --name feature-worker --role worker "Implement feature X"

# 3. Prophet vérifie le status
./tickets list
./tickets show abc123

# 4. Worker marque comme terminé
./tickets update abc123 --status done
```
