# Ticket Management

Gestion des tickets pour tracker les tâches déléguées.

## Actions disponibles

Demander à l'utilisateur quelle action :

### 1. Créer un ticket
```bash
./tickets create "<title>" --body "<description>"
# Ou avec assignation immédiate :
./tickets create "<title>" --assign <worker-name>
```

### 2. Lister les tickets
```bash
./tickets list
# Filtrer par status :
./tickets list --status open
./tickets list --status in-progress
./tickets list --status blocked
./tickets list --status done
```

### 3. Voir un ticket
```bash
./tickets show <ticket-id>
# Supporte les IDs partiels : ./tickets show abc
```

### 4. Assigner un worker
```bash
./tickets assign <ticket-id> <worker-name>
# Note: passe automatiquement en "in-progress" si "open"
```

### 5. Mettre à jour le status
```bash
./tickets update <ticket-id> --status done
./tickets update <ticket-id> --status blocked
./tickets update <ticket-id> --status in-progress
```

### 6. Ajouter un commentaire
```bash
./tickets comment <ticket-id> "Progress update message"
```

### 7. Statistiques
```bash
./tickets stats
```

## Workflow typique

1. Créer ticket → 2. Assigner worker → 3. Spawner worker → 4. Superviser → 5. Marquer done

## États des tickets

| État | Icône | Description |
|------|-------|-------------|
| open | ○ | Nouveau, pas assigné |
| in-progress | ◐ | En cours |
| blocked | ✗ | Bloqué |
| done | ✓ | Terminé |
