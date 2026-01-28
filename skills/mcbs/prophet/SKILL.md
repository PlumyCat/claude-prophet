---
name: prophet
description: Prophet Claude Management
allowed-tools: Bash
---

# Prophet Claude Management

Gère le (re)démarrage de Prophet Claude dans une session tmux dédiée.

## Lancer/Relancer Prophet Claude

```bash
/home/eric/projects/twich-test/restart-prophet-claude.sh
```

Le chemin absolu permet de lancer depuis n'importe quel dossier.

Ce script :
1. Génère `settings.json` depuis context-cli avec le rôle prophet-claude
2. Tue l'ancienne session tmux si elle existe
3. Démarre une nouvelle session `prophet-claude` avec Claude
4. Envoie le prompt d'initialisation

## Commandes utiles

```bash
# Voir si Prophet Claude tourne
tmux has-session -t prophet-claude 2>/dev/null && echo "Running" || echo "Not running"

# Attacher à la session
tmux attach -t prophet-claude

# Voir l'état sans attacher
tmux capture-pane -t prophet-claude -p | tail -20

# Tuer la session
tmux kill-session -t prophet-claude
```

## Architecture

```
Toi (terminal normal)
  └── claude -c (cette conversation = Prophet)
        ├── /spawn worker-1 → tmux session
        ├── /spawn worker-2 → tmux session
        └── /spawn worker-3 → tmux session
```

Prophet Claude peut aussi tourner dans tmux pour des sessions longues autonomes.
