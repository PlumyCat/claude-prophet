# Spawn Worker

Crée un nouveau worker Claude dans une session tmux isolée.

## Paramètres à collecter

1. **Nom** (optionnel) : Nom descriptif pour le worker
   - Si non fourni, un ID unique sera généré
   - Exemples : `auth-backend`, `test-runner`, `docs-writer`

2. **Rôle** (optionnel) : Contexte prédéfini à charger
   - Lister les rôles disponibles : `./context list-roles`
   - Rôles courants : `worker`, `prophet-claude`

3. **Ticket** (optionnel) : ID du ticket à associer
   - Le ticket sera automatiquement assigné au worker
   - Le worker recevra l'ID dans son contexte

4. **Tâche** (requis) : Le prompt/instruction pour le worker

## Commande à exécuter

```bash
# Basique
./claude spawn --name <name> "<task>"

# Avec rôle
./claude spawn --name <name> --role worker "<task>"

# Avec ticket (recommandé)
./claude spawn --name <name> --role worker --ticket <ticket-id> "<task>"
```

## Workflow recommandé (avec ticket)

```bash
# 1. Créer le ticket
./tickets create "<task-title>"
# → Ticket #abc123 created

# 2. Spawner avec le ticket
./claude spawn --name my-worker --role worker --ticket abc123 "<task-details>"
# → Le ticket est auto-assigné au worker
# → Le worker connait son ticket ID

# 3. Vérifier
./claude list
./tickets list
```

## Notes importantes

- Les workers sont lancés avec `--dangerously-skip-permissions` pour l'autonomie
- Le rôle `worker` inclut des instructions de fin de tâche (update ticket + /exit)
- Le ticket est auto-assigné et passe en "in-progress" au spawn

## Bonnes pratiques

- Utiliser des noms descriptifs (pas `worker1`, `test`)
- Toujours utiliser `--role worker` pour le contexte approprié
- Lier un ticket pour le tracking (`--ticket`)
- Donner des instructions claires et complètes
- Préciser les fichiers concernés
