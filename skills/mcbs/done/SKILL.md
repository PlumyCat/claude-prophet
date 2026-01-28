---
name: done
description: Done - Task Completion
allowed-tools: Bash
---

# Done - Task Completion

Signale la fin d'une tâche assignée à un worker.

## Utilisation

Ce skill est destiné aux **workers** pour signaler qu'ils ont terminé leur tâche.

## Actions à effectuer

### 1. Demander le ticket ID (si pas connu)

### 2. Mettre à jour le ticket
```bash
/home/eric/projects/twich-test/tickets update <ticket-id> --status done
/home/eric/projects/twich-test/tickets comment <ticket-id> "Task completed by worker"
```

### 3. Rappeler /exit

IMPORTANT: Toujours rappeler au worker de faire `/exit` pour libérer la session tmux.

## Workflow

```
Worker termine sa tâche
       │
       ▼
   /done <ticket-id>
       │
       ├─► tickets update → done
       ├─► tickets comment → "Completed"
       │
       ▼
   Rappel: /exit
       │
       ▼
   Worker fait /exit
       │
       ▼
   Session tmux libérée
```

## Notes

- Ce skill ne fait PAS `/exit` automatiquement
- Si pas de ticket, juste rappeler de faire `/exit`
