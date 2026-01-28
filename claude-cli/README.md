# claude-cli

CLI pour spawner et gérer des workers Claude dans des sessions tmux.

## Installation

```bash
cd claude-cli
uv sync
```

## Commandes

### spawn

Crée un nouveau worker Claude dans une session tmux.

```bash
# Spawn basique (nom auto-généré)
uv run python main.py spawn "Implémente une fonction fibonacci"

# Spawn avec nom personnalisé
uv run python main.py spawn --name fib-worker "Implémente fibonacci"

# Spawn avec un rôle (requiert context-cli)
uv run python main.py spawn --role worker "Fix le bug dans auth.py"
```

### capture

Capture la sortie d'un worker.

```bash
# Capture les 30 dernières lignes (défaut)
uv run python main.py capture my-worker

# Capture les 100 dernières lignes
uv run python main.py capture my-worker --lines 100
```

### list

Liste tous les workers actifs.

```bash
uv run python main.py list
```

### kill

Termine un worker spécifique.

```bash
uv run python main.py kill my-worker
```

### kill-all

Termine tous les workers Claude.

```bash
# Avec confirmation
uv run python main.py kill-all

# Sans confirmation
uv run python main.py kill-all --force
```

### send

Envoie du texte à un worker (avancé).

```bash
# Envoyer /exit pour terminer
uv run python main.py send my-worker "/exit"

# Envoyer une instruction supplémentaire
uv run python main.py send my-worker "Continue avec l'étape suivante"
```

## Exemple de workflow

```bash
# 1. Spawner un worker
uv run python main.py spawn --name auth-impl "Implémente l'authentification JWT"

# 2. Vérifier qu'il tourne
uv run python main.py list

# 3. Voir sa progression
uv run python main.py capture auth-impl --lines 50

# 4. Quand terminé, nettoyer
uv run python main.py kill auth-impl
```

## Notes

- Les sessions sont préfixées par `claude-`
- Utilisez `capture` plutôt que `tmux attach` pour surveiller
- Les workers peuvent auto-terminer avec `/exit`
