---
name: status
description: System Status
allowed-tools: Bash
---

# System Status

Vue d'ensemble du système Multi-Claude Bootstrap.

## Commandes à exécuter

### 1. Status Prophet Claude
```bash
tmux has-session -t prophet-claude 2>/dev/null && echo "Prophet Claude: RUNNING" || echo "Prophet Claude: STOPPED"
```

### 2. Workers actifs
```bash
/home/eric/projects/twich-test/claude list
```

### 3. Tickets en cours
```bash
/home/eric/projects/twich-test/tickets list --status in-progress
/home/eric/projects/twich-test/tickets list --status blocked
```

### 4. Statistiques tickets
```bash
/home/eric/projects/twich-test/tickets stats
```

## Format de sortie

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

- Prophet STOPPED → `/prophet`
- Tickets BLOCKED → Investiguer
- Pas de workers mais tickets in-progress → Vérifier `/capture`
