# Prophet Claude Management

Gestion de la session Prophet Claude (orchestrateur principal).

## Actions disponibles

Demande à l'utilisateur quelle action effectuer :

1. **start** - Démarrer Prophet Claude (si pas déjà actif)
2. **restart** - Redémarrer Prophet Claude (kill + start)
3. **status** - Vérifier le status de Prophet Claude
4. **attach** - Afficher la commande pour s'attacher

## Implémentation

### Status
```bash
tmux has-session -t prophet-claude 2>/dev/null && echo "Prophet Claude: RUNNING" || echo "Prophet Claude: STOPPED"
```

### Start
```bash
./restart-prophet-claude.sh
```

### Attach info
Afficher :
```
Pour s'attacher à Prophet Claude :
  tmux attach -t prophet-claude

Pour se détacher : Ctrl+B puis D
```

## Contexte

Prophet Claude est l'orchestrateur qui :
- Reçoit les demandes de l'humain
- Délègue aux workers via `./claude spawn`
- Supervise avec `./claude capture`
- Tracke les tâches avec `./tickets`
