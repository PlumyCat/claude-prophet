# System Status

Vue d'ensemble du système Multi-Claude Bootstrap.

## Commandes à exécuter

### 1. Status Prophet Claude
```bash
tmux has-session -t prophet-claude 2>/dev/null && echo "Prophet Claude: RUNNING" || echo "Prophet Claude: STOPPED"
```

### 2. Workers actifs
```bash
./claude list
```

### 3. Tickets en cours
```bash
./tickets list --status in-progress
./tickets list --status blocked
```

### 4. Statistiques tickets
```bash
./tickets stats
```

## Format de sortie suggéré

```
=== Multi-Claude System Status ===

Prophet Claude: [RUNNING/STOPPED]

Workers actifs: X
  - worker-1 (running)
  - worker-2 (running)

Tickets:
  ○ Open: X
  ◐ In-progress: X
  ✗ Blocked: X
  ✓ Done: X

Sessions tmux: X total
```

## Actions recommandées

Si Prophet Claude est STOPPED :
→ Suggérer `/prophet` pour le démarrer

Si des tickets sont BLOCKED :
→ Lister les tickets bloqués et suggérer d'investiguer

Si aucun worker actif mais tickets in-progress :
→ Les workers ont peut-être terminé, vérifier avec `/capture`
