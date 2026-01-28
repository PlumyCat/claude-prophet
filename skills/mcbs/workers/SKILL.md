---
name: workers
description: Workers Management
allowed-tools: Bash
---

# Workers Management

Liste et gère les workers Claude actifs.

## Commandes

### Lister les workers actifs
```bash
/home/eric/projects/twich-test/claude list
```

### Voir toutes les sessions tmux
```bash
tmux list-sessions 2>/dev/null || echo "Aucune session tmux active"
```

## Format de sortie

Pour chaque worker, afficher :
- Nom de la session
- Status (running/stopped)
- Durée d'activité

## Actions rapides

1. Capturer la sortie : `/capture <name>`
2. Tuer un worker : `/kill <name>`
3. Tuer tous : `./claude kill-all`
4. Nouveau worker : `/spawn`

## Notes

- Sessions Claude préfixées avec `claude-` sauf si nommées explicitement
- Prophet Claude : session `prophet-claude`
