# Spawn Worker

Crée un nouveau worker Claude dans une session tmux isolée.

## Paramètres à collecter

1. **Nom** (optionnel) : Nom descriptif pour le worker
   - Si non fourni, un ID unique sera généré
   - Exemples : `auth-backend`, `test-runner`, `docs-writer`

2. **Rôle** (optionnel) : Contexte prédéfini à charger
   - Lister les rôles disponibles : `./context list-roles`
   - Rôles courants : `worker`, `prophet-claude`

3. **Tâche** (requis) : Le prompt/instruction pour le worker

## Commande à exécuter

```bash
# Sans rôle
./claude spawn --name <name> "<task>"

# Avec rôle
./claude spawn --name <name> --role <role> "<task>"
```

## Workflow recommandé

1. Créer un ticket pour tracker la tâche :
   ```bash
   ./tickets create "<task-title>" --assign <worker-name>
   ```

2. Spawner le worker :
   ```bash
   ./claude spawn --name <worker-name> --role worker "<task-details>"
   ```

3. Vérifier le démarrage :
   ```bash
   ./claude list
   ```

## Bonnes pratiques

- Utiliser des noms descriptifs (pas `worker1`, `test`)
- Donner des instructions claires et complètes
- Préciser les fichiers concernés
- Indiquer de sortir avec `/exit` quand terminé
