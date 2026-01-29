---
name: mcbs-ticket
description: Ticket Management
allowed-tools: Bash
---

# Ticket Management

Gestion des tickets pour tracker les tâches déléguées.

## Actions disponibles

### 1. Créer un ticket
```bash
/home/eric/projects/twich-test/tickets create "<title>" --body "<description>"
# Avec assignation :
/home/eric/projects/twich-test/tickets create "<title>" --assign <worker-name>
```

### 2. Lister les tickets
```bash
/home/eric/projects/twich-test/tickets list
# Filtrer :
/home/eric/projects/twich-test/tickets list --status open
/home/eric/projects/twich-test/tickets list --status in-progress
/home/eric/projects/twich-test/tickets list --status blocked
/home/eric/projects/twich-test/tickets list --status done
```

### 3. Voir un ticket
```bash
/home/eric/projects/twich-test/tickets show <ticket-id>
```

### 4. Assigner un worker
```bash
/home/eric/projects/twich-test/tickets assign <ticket-id> <worker-name>
```

### 5. Mettre à jour le status
```bash
/home/eric/projects/twich-test/tickets update <ticket-id> --status done
/home/eric/projects/twich-test/tickets update <ticket-id> --status blocked
```

### 6. Ajouter un commentaire
```bash
/home/eric/projects/twich-test/tickets comment <ticket-id> "Progress update"
```

### 7. Statistiques
```bash
/home/eric/projects/twich-test/tickets stats
```

## États des tickets

| État | Icône | Description |
|------|-------|-------------|
| open | ○ | Nouveau, pas assigné |
| in-progress | ◐ | En cours |
| blocked | ✗ | Bloqué |
| done | ✓ | Terminé |
