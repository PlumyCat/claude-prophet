# Workers Management

Liste et gère les workers Claude actifs.

## Commandes à exécuter

### Lister les workers actifs
```bash
./claude list
```

### Voir toutes les sessions tmux (incluant non-claude)
```bash
tmux list-sessions 2>/dev/null || echo "Aucune session tmux active"
```

## Informations à afficher

Pour chaque worker, montrer :
- Nom de la session
- Status (running/stopped)
- Durée d'activité si disponible

## Actions rapides

Proposer à l'utilisateur :
1. Capturer la sortie d'un worker (`./claude capture <name>`)
2. Tuer un worker (`./claude kill <name>`)
3. Tuer tous les workers (`./claude kill-all`)
4. Spawner un nouveau worker (utiliser `/spawn`)

## Notes

Les sessions Claude sont préfixées avec `claude-` sauf si nommées explicitement.
Prophet Claude a sa propre session `prophet-claude`.
