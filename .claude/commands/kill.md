# Kill Workers

Termine un ou plusieurs workers Claude.

## Actions disponibles

### 1. Tuer un worker spécifique
```bash
./claude kill <worker-name>
```

### 2. Tuer tous les workers
```bash
./claude kill-all
# Avec confirmation skip :
./claude kill-all --force
```

## Avant de tuer

1. Vérifier les workers actifs :
   ```bash
   ./claude list
   ```

2. Capturer la sortie si besoin de récupérer le travail :
   ```bash
   ./claude capture <worker-name> --lines 1000
   ```

3. Mettre à jour le ticket associé si applicable :
   ```bash
   ./tickets update <ticket-id> --status blocked
   ./tickets comment <ticket-id> "Worker killed - reason: ..."
   ```

## Cas d'usage

- **Worker bloqué** : Ne répond plus ou en boucle
- **Mauvaise tâche** : Instructions incorrectes, besoin de respawner
- **Nettoyage** : Fin de session, libérer les ressources
- **Erreur** : Worker en erreur, besoin de relancer

## Notes

- `kill` ne supprime pas les tickets associés
- Les workers terminent normalement avec `/exit`
- `kill-all` ne tue PAS la session `prophet-claude`
