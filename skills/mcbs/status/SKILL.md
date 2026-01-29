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

### 5. Workers en attente de réponse
```bash
echo "=== Workers en attente ==="
ls /home/eric/projects/twich-test/signals/waiting/*.json 2>/dev/null || echo "Aucun worker en attente"
```

```bash
# Détails des tickets waiting
/home/eric/projects/twich-test/tickets list --status waiting
```

```bash
# Voir le détail des signals (si présents)
for f in /home/eric/projects/twich-test/signals/waiting/*.json; do
  [ -f "$f" ] && echo "--- $(basename $f .json) ---" && cat "$f"
done 2>/dev/null
```

## Format de sortie

```
=== Multi-Claude System Status ===

Prophet Claude: [RUNNING/STOPPED]

Workers actifs: X
  - worker-1 (running)
  - worker-2 (running)

Workers en attente: X
  ⏳ claude-auth: "OAuth ou JWT?" (ticket abc123)

Tickets:
  ○ Open: X
  ◐ In-progress: X
  ✗ Blocked: X
  ⏳ Waiting: X
  ✓ Done: X

Sessions tmux: X total
```

## Actions recommandées

- Prophet STOPPED → `/prophet`
- Tickets BLOCKED → Investiguer
- Tickets WAITING → `/mcbs:respond <session> "réponse"`
- Pas de workers mais tickets in-progress → Vérifier `/capture`
