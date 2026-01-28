# Multi-Claude Bootstrap System - Guide d'Utilisation

> Documentation complète du système d'orchestration multi-agents Claude

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Concepts Clés](#concepts-clés)
6. [Workflows](#workflows)
7. [Référence des Commandes](#référence-des-commandes)
8. [Bonnes Pratiques](#bonnes-pratiques)
9. [Troubleshooting](#troubleshooting)

---

## Vue d'ensemble

### Qu'est-ce que le Multi-Claude Bootstrap ?

Un système permettant d'orchestrer **plusieurs instances Claude** travaillant en parallèle. Un Claude principal ("Prophet Claude") délègue des tâches à des workers isolés dans des sessions tmux.

### Pourquoi utiliser ce système ?

| Problème | Solution |
|----------|----------|
| Tâches complexes = contexte saturé | Déléguer à des workers spécialisés |
| Travail séquentiel = lent | Workers parallèles asynchrones |
| Contexte perdu au restart | Rôles et directives persistants |
| Pas de tracking des tâches | Système de tickets intégré |

### Cas d'usage

- **Développement parallèle** : Un worker sur le backend, un sur le frontend
- **Code review** : Worker spécialisé avec directives de review
- **Refactoring massif** : Plusieurs workers sur différents modules
- **Documentation** : Worker dédié à la génération de docs

---

## Architecture

### Diagramme Global

```
┌─────────────────────────────────────────────────────────────────┐
│                         HUMAN                                   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   PROPHET CLAUDE                        │    │
│  │                   (Orchestrateur)                       │    │
│  │                                                         │    │
│  │  • Reçoit les demandes humaines                         │    │
│  │  • Décompose en sous-tâches                             │    │
│  │  • Délègue aux workers                                  │    │
│  │  • Supervise et intègre                                 │    │
│  │                                                         │    │
│  │  Outils: claude-cli, context-cli, tickets-cli           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                     │
│            ┌──────────────┼──────────────┐                      │
│            │              │              │                      │
│            ▼              ▼              ▼                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │   WORKER 1   │ │   WORKER 2   │ │   WORKER N   │             │
│  │   (tmux)     │ │   (tmux)     │ │   (tmux)     │             │
│  │              │ │              │ │              │             │
│  │ • Tâche      │ │ • Tâche      │ │ • Tâche      │             │
│  │   spécifique │ │   spécifique │ │   spécifique │             │
│  │ • Contexte   │ │ • Contexte   │ │ • Contexte   │             │
│  │   isolé      │ │   isolé      │ │   isolé      │             │
│  │ • Auto-exit  │ │ • Auto-exit  │ │ • Auto-exit  │             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Composants

```
bootstrap/
│
├── claude-cli/          # Gestion des workers tmux
│   ├── spawn            # Créer un worker
│   ├── capture          # Voir la sortie
│   ├── list             # Lister les workers
│   └── kill             # Terminer un worker
│
├── context-cli/         # Gestion des contextes
│   ├── roles/           # Définitions des rôles
│   ├── directives/      # Règles réutilisables
│   ├── show             # Afficher un contexte
│   └── settings         # Générer settings.json
│
├── tickets-cli/         # Tracking des tâches
│   ├── tickets/         # Stockage JSON
│   ├── create           # Créer un ticket
│   ├── assign           # Assigner un worker
│   └── update           # Changer le statut
│
└── scripts/
    └── restart-prophet-claude.sh
```

### Flux de Données

```
                    ┌─────────────┐
                    │ context-cli │
                    │             │
                    │ roles/      │
                    │ directives/ │
                    └──────┬──────┘
                           │
                           │ génère contexte
                           ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ tickets-cli │◄────│ claude-cli  │────►│    tmux     │
│             │     │             │     │             │
│ • tracking  │     │ • spawn     │     │ • sessions  │
│ • états     │     │ • capture   │     │ • isolation │
│ • historique│     │ • kill      │     │ • send-keys │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Installation

### Prérequis

```bash
# Python 3.11+
python3 --version  # >= 3.11

# uv (gestionnaire de paquets Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# tmux
sudo apt install tmux  # Ubuntu/Debian
brew install tmux      # macOS

# Claude Code CLI
# Doit être installé et configuré avec un compte actif
claude --version
```

### Installation du système

```bash
# Cloner ou créer le dossier
mkdir -p ~/workspace/bootstrap
cd ~/workspace/bootstrap

# Initialiser claude-cli
mkdir claude-cli && cd claude-cli
uv init
uv add click
# ... copier main.py

# Initialiser context-cli
cd .. && mkdir context-cli && cd context-cli
uv init
uv add click pyyaml
# ... copier main.py et créer roles/, directives/

# Initialiser tickets-cli (optionnel)
cd .. && mkdir tickets-cli && cd tickets-cli
uv init
uv add click
# ... copier main.py

# Créer les wrapper scripts
cd ..
# ... créer claude, context, tickets scripts
chmod +x claude context tickets restart-prophet-claude.sh
```

---

## Quick Start

### 1. Démarrer Prophet Claude

```bash
cd ~/workspace/bootstrap
./restart-prophet-claude.sh

# Ou manuellement :
tmux new-session -d -s prophet-claude "claude"
tmux attach -t prophet-claude
```

### 2. Déléguer votre première tâche

Dans Prophet Claude :

```bash
# Spawner un worker
./claude spawn --name hello-worker "Say 'Hello World' and then exit with /exit"

# Vérifier qu'il tourne
./claude list

# Voir sa sortie
./claude capture hello-worker

# Nettoyer
./claude kill hello-worker
```

### 3. Utiliser les rôles

```bash
# Voir les rôles disponibles
./context list-roles

# Spawner avec un rôle
./claude spawn --role worker --name code-worker "Implement a fibonacci function in Python"

# Le worker reçoit le contexte du rôle "worker"
```

---

## Concepts Clés

### Prophet Claude vs Workers

| Aspect | Prophet Claude | Worker Claude |
|--------|----------------|---------------|
| **Rôle** | Orchestrateur | Exécutant |
| **Durée de vie** | Permanent | Temporaire |
| **Contexte** | Complet (système) | Spécialisé (tâche) |
| **Actions** | Déléguer, superviser | Implémenter, reporter |
| **Session tmux** | `prophet-claude` | `claude-XXXXXXXX` |

### Sessions tmux

```
┌─────────────────────────────────────────────────────┐
│ tmux server                                         │
│                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐   │
│  │ prophet-claude      │  │ claude-abc12345     │   │
│  │ (attached)          │  │ (detached)          │   │
│  │                     │  │                     │   │
│  │ Human ◄──► Claude   │  │ Worker Claude       │   │
│  │                     │  │ (autonome)          │   │
│  └─────────────────────┘  └─────────────────────┘   │
│                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐   │
│  │ claude-def67890     │  │ claude-ghi11111     │   │
│  │ (detached)          │  │ (detached)          │   │
│  └─────────────────────┘  └─────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Rôles et Directives

```yaml
# Structure d'un rôle
roles/worker.yaml:
  name: worker
  description: "Worker pour tâches déléguées"
  prompt: |
    Tu es un Worker Claude. Complète la tâche et sors.

    CONTRAINTES:
    - Focus sur la tâche donnée
    - Ne démarre pas de nouvelles tâches
    - Sors avec /exit quand terminé

  directives:
    - base           # Inclut directives/base.yaml
    - code-quality   # Inclut directives/code-quality.yaml

# Structure d'une directive
directives/code-quality.yaml:
  name: code-quality
  description: "Standards de qualité du code"
  content: |
    ## Standards de Code
    - Tests pour chaque fonction
    - Noms descriptifs
    - Pas de code mort
```

### Système de Tickets

```
┌─────────────────────────────────────────────────────────┐
│                    TICKET LIFECYCLE                     │
│                                                         │
│   ┌──────┐    ┌─────────────┐    ┌─────────┐    ┌────┐  │
│   │ OPEN │───►│IN-PROGRESS  │───►│ BLOCKED │───►│DONE│  │
│   └──────┘    └─────────────┘    └─────────┘    └────┘  │
│       │              │                 │           ▲    │
│       │              │                 │           │    │
│       └──────────────┴─────────────────┴───────────┘    │
│                                                         │
│   create          assign            update       update │
│                   (auto)                                │
└─────────────────────────────────────────────────────────┘
```

---

## Workflows

### Workflow Basique : Délégation Simple

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Human demande une tâche complexe                    │
│     │                                                   │
│     ▼                                                   │
│  2. Prophet Claude analyse et décompose                 │
│     │                                                   │
│     ├─────────────────────────────────────────┐         │
│     ▼                                         ▼         │
│  3. ./claude spawn "Sous-tâche 1"    ./claude spawn "Sous-tâche 2"
│     │                                         │         │
│     ▼                                         ▼         │
│  4. Worker 1 exécute                 Worker 2 exécute   │
│     │                                         │         │
│     ▼                                         ▼         │
│  5. ./claude capture worker1    ./claude capture worker2│
│     │                                         │         │
│     └─────────────────┬───────────────────────┘         │
│                       ▼                                 │
│  6. Prophet Claude intègre les résultats                │
│     │                                                   │
│     ▼                                                   │
│  7. Human reçoit le livrable complet                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Workflow Avancé : Avec Tickets

```bash
# Prophet Claude reçoit : "Ajoute l'authentification JWT"

# 1. Créer le ticket
./tickets create "Implement JWT Auth" --body "Backend + Frontend"

# 2. Spawner et assigner
./claude spawn --role worker --name auth-backend "Implement JWT backend"
./tickets assign <ticket-id> auth-backend

# 3. Superviser
./claude capture auth-backend --lines 50
./tickets show <ticket-id>

# 4. Quand terminé
./tickets update <ticket-id> --status done
```

### Workflow : Code Review

```bash
# Définir un rôle reviewer
# context-cli/roles/code-reviewer.yaml

# Spawner le reviewer
./claude spawn --role code-reviewer --name reviewer-pr123 \
  "Review the changes in src/auth.py for security issues"

# Capturer le rapport
./claude capture reviewer-pr123 > review-report.md
```

---

## Référence des Commandes

### claude-cli

| Commande | Description | Exemple |
|----------|-------------|---------|
| `spawn` | Crée un worker | `./claude spawn "task"` |
| `spawn --name` | Worker nommé | `./claude spawn --name my-worker "task"` |
| `spawn --role` | Avec un rôle | `./claude spawn --role worker "task"` |
| `capture` | Voir la sortie | `./claude capture my-worker` |
| `capture --lines` | N dernières lignes | `./claude capture my-worker --lines 100` |
| `list` | Lister les workers | `./claude list` |
| `kill` | Tuer un worker | `./claude kill my-worker` |
| `kill-all` | Tuer tous | `./claude kill-all --force` |

### context-cli

| Commande | Description | Exemple |
|----------|-------------|---------|
| `show` | Affiche le contexte | `./context show worker` |
| `list-roles` | Liste les rôles | `./context list-roles` |
| `list-directives` | Liste les directives | `./context list-directives` |
| `settings` | Génère settings.json | `./context settings prophet-claude` |

### tickets-cli

| Commande | Description | Exemple |
|----------|-------------|---------|
| `create` | Crée un ticket | `./tickets create "Title"` |
| `create --body` | Avec description | `./tickets create "Title" --body "Details"` |
| `create --assign` | Création + assignation | `./tickets create "Title" --assign worker` |
| `list` | Liste les tickets | `./tickets list` |
| `list --status` | Filtré par état | `./tickets list --status open` |
| `list --assigned` | Filtré par worker | `./tickets list --assigned my-worker` |
| `show` | Détail d'un ticket | `./tickets show abc123` |
| `assign` | Assigne un worker | `./tickets assign abc123 my-worker` |
| `update --status` | Change l'état | `./tickets update abc123 --status done` |
| `comment` | Ajoute un commentaire | `./tickets comment abc123 "Progress update"` |
| `delete` | Supprime un ticket | `./tickets delete abc123 --force` |
| `stats` | Statistiques globales | `./tickets stats` |

---

## Bonnes Pratiques

### Pour Prophet Claude

```
✅ DO:
- Déléguer les tâches non-triviales
- Donner des instructions claires aux workers
- Vérifier régulièrement avec capture
- Utiliser des noms de session descriptifs

❌ DON'T:
- Faire le travail d'implémentation
- Attendre qu'un worker finisse (non-bloquant)
- Tuer manuellement les sessions tmux
- S'attacher aux sessions workers
```

### Pour les Workers

```
✅ DO:
- Se concentrer sur la tâche assignée
- Sortir avec /exit quand terminé
- Reporter les blocages clairement

❌ DON'T:
- Démarrer de nouvelles tâches non demandées
- Modifier des fichiers hors scope
- Rester actif après avoir terminé
```

### Nommage des Sessions

```
Bon:
- auth-backend-worker
- feature-42-implementation
- code-review-pr-123

Mauvais:
- worker1
- test
- claude-session
```

---

## Troubleshooting

### "Session not found"

```bash
# Vérifier les sessions existantes
tmux list-sessions

# Le worker a peut-être terminé (auto-exit)
# Relancer si nécessaire
./claude spawn --name <name> "task"
```

### "No active workers"

```bash
# Normal si tous ont terminé avec /exit
# Vérifier l'historique tmux
tmux list-sessions -a
```

### Worker bloqué

```bash
# Capturer pour voir l'état
./claude capture <worker> --lines 100

# Si vraiment bloqué, tuer et respawner
./claude kill <worker>
./claude spawn --name <worker> "task corrigée"
```

### Contexte non appliqué

```bash
# Vérifier que le rôle existe
./context list-roles

# Vérifier le contenu du rôle
./context show <role>

# Regénérer settings.json si nécessaire
./context settings <role> > settings.json
```

---

## Annexes

### Commandes tmux Utiles

```bash
# Lister les sessions
tmux list-sessions

# S'attacher à une session (debug uniquement)
tmux attach -t <session>

# Détacher (Ctrl+B puis D)

# Capturer manuellement
tmux capture-pane -t <session> -p

# Envoyer une commande
tmux send-keys -t <session> "commande" Enter
```

### Exemple de Session Complète

```bash
# Terminal 1 : Prophet Claude
./restart-prophet-claude.sh
tmux attach -t prophet-claude

# Dans Prophet Claude :
> Implémente un système de cache Redis pour l'API

# Prophet répond et délègue :
./claude spawn --role worker --name cache-impl \
  "Implement Redis caching in src/api/cache.py:
   - Connection pool
   - get/set methods
   - TTL support
   - Error handling"

./claude spawn --role worker --name cache-tests \
  "Write tests for Redis cache in tests/test_cache.py"

# Prophet vérifie :
./claude list
# cache-impl (running)
# cache-tests (running)

./claude capture cache-impl --lines 30
# ... voir la progression ...

# Quand terminé :
./claude capture cache-impl > /tmp/cache-impl-result.md
./claude capture cache-tests > /tmp/cache-tests-result.md

# Intégrer et continuer
```

---

*Documentation générée à partir du tutoriel Multi-Claude Bootstrap de @claudecodeonly*
*Dernière mise à jour : 2025-01-28*
