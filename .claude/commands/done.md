# Done - Task Completion

Signale la fin d'une tâche assignée à un worker.

## Utilisation

Ce skill est destiné aux **workers** pour signaler qu'ils ont terminé leur tâche.

## Actions à effectuer

### 1. Demander le ticket ID (si pas connu)

Si l'utilisateur n'a pas mentionné de ticket, demander :
- "Quel est l'ID du ticket associé à cette tâche ?"
- Ou vérifier s'il y a un ticket mentionné dans le contexte

### 2. Mettre à jour le ticket

```bash
./tickets update <ticket-id> --status done
./tickets comment <ticket-id> "Task completed by worker"
```

### 3. Afficher confirmation

```
✓ Ticket <id> marqué comme terminé
✓ Tâche complétée avec succès

Pour libérer cette session, exécute: /exit
```

### 4. Rappeler /exit

IMPORTANT: Toujours rappeler au worker de faire `/exit` pour libérer la session tmux.

## Workflow complet

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

## Exemple

```
Worker: J'ai terminé l'implémentation de la fonction fibonacci.

> /done abc123

✓ Ticket abc123 marqué comme terminé
✓ Commentaire ajouté: "Task completed by worker"

Pour libérer cette session, exécute maintenant: /exit
```

## Notes

- Ce skill ne fait PAS `/exit` automatiquement (pour laisser le worker vérifier)
- Le ticket doit exister sinon erreur
- Si pas de ticket, juste rappeler de faire `/exit`
