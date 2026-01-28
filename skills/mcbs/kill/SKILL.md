---
name: kill
description: Kill Workers
allowed-tools: Bash
---

# Kill Workers

Termine un ou plusieurs workers Claude.

## Commandes

### Tuer un worker spécifique
```bash
/home/eric/projects/twich-test/claude kill <worker-name>
```

### Tuer tous les workers
```bash
/home/eric/projects/twich-test/claude kill-all
# Avec confirmation skip :
/home/eric/projects/twich-test/claude kill-all --force
```

## Avant de tuer

1. Vérifier les workers actifs :
   ```bash
   /home/eric/projects/twich-test/claude list
   ```

2. Capturer la sortie si besoin :
   ```bash
   /home/eric/projects/twich-test/claude capture <worker-name> --lines 1000
   ```

3. Mettre à jour le ticket si applicable :
   ```bash
   /home/eric/projects/twich-test/tickets update <ticket-id> --status blocked
   ```

## Cas d'usage

- **Worker bloqué** : Ne répond plus ou en boucle
- **Mauvaise tâche** : Instructions incorrectes
- **Nettoyage** : Fin de session
- **Erreur** : Worker en erreur

## Notes

- `kill` ne supprime pas les tickets associés
- Workers terminent normalement avec `/exit`
- `kill-all` ne tue PAS `prophet-claude`
