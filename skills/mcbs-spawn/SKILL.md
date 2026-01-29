---
name: mcbs-spawn
description: Spawn Worker
allowed-tools: Bash
---

# Spawn Worker

Crée un nouveau worker Claude dans une session tmux isolée.

## Paramètres à collecter

1. **Nom** (optionnel) : Nom descriptif pour le worker
2. **Rôle** (optionnel) : Contexte prédéfini (`worker`, `prophet-claude`)
3. **Ticket** (optionnel) : ID du ticket à associer
4. **Skill** (optionnel) : Skills à activer au démarrage (répétable)
5. **Tâche** (requis) : Le prompt/instruction pour le worker

## Commandes

```bash
# Basique
/home/eric/projects/twich-test/claude spawn --name <name> "<task>"

# Avec rôle (recommandé)
/home/eric/projects/twich-test/claude spawn --name <name> --role worker "<task>"

# Avec ticket (recommandé pour tracking)
/home/eric/projects/twich-test/claude spawn --name <name> --role worker --ticket <ticket-id> "<task>"

# Avec skills (pour autonomie)
/home/eric/projects/twich-test/claude spawn --skill ralph-loop:ralph-loop "<task>"

# Combiner plusieurs skills
/home/eric/projects/twich-test/claude spawn -s bmad:dev-story -s ralph-loop:ralph-loop "<task>"
```

## Mode Ralph Loop (--ralph)

Pour une exécution autonome sans intervention :

```bash
/home/eric/projects/twich-test/claude spawn --ralph "Tâche longue à exécuter"
/home/eric/projects/twich-test/claude spawn --ralph --role worker --ticket abc123 "Feature complète"
```

Note: Éviter les parenthèses `()` dans le prompt avec --ralph (problème d'échappement bash).

## Skills utiles pour workers

| Skill | Effet |
|-------|-------|
| `ralph-loop:ralph-loop` | Continue automatiquement sans attendre |
| `bmad:dev-story` | Workflow développement structuré |
| `epct` | Explore-Plan-Code-Test workflow |

## Workflow recommandé

```bash
# 1. Créer le ticket
/home/eric/projects/twich-test/tickets create "<task-title>"

# 2. Spawner avec le ticket
/home/eric/projects/twich-test/claude spawn --name my-worker --role worker --ticket abc123 "<task>"

# 3. Vérifier
/home/eric/projects/twich-test/claude list
```

## Notes

- Workers lancés avec `--dangerously-skip-permissions` pour l'autonomie
- Le rôle `worker` inclut instructions de fin (update ticket + /exit)
- Utiliser des noms descriptifs et instructions claires
