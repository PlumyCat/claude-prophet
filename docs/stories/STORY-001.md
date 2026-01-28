# STORY-001: Multi-Claude Bootstrap System

**Epic:** Multi-Agent Orchestration
**Priority:** Must Have
**Story Points:** 13 (à décomposer en sous-stories)
**Status:** Not Started
**Assigned To:** Unassigned
**Created:** 2025-01-28
**Sprint:** 1

---

## User Story

As a **développeur solo**
I want to **orchestrer plusieurs instances Claude via tmux**
So that **je puisse déléguer des tâches à des workers Claude spécialisés et multiplier ma productivité**

---

## Description

### Background
Le tutoriel de @claudecodeonly (6h sur Twitch) démontre un pattern avancé d'orchestration multi-agents Claude. Le système permet à un "Prophet Claude" principal de déléguer des tâches à des workers Claude isolés dans des sessions tmux, créant un flux de travail parallèle et asynchrone.

### Architecture Cible

```
                    ┌─────────────────┐
                    │  Prophet Claude │ ← Interface humaine
                    │   (Principal)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Worker  │  │  Worker  │  │  Manager │
        │  (tmux)  │  │  (tmux)  │  │  (tmux)  │
        └──────────┘  └──────────┘  └──────────┘
```

### Composants Principaux

1. **claude-cli** - CLI Python pour spawner/gérer les workers
   - `spawn` : Créer un worker dans une session tmux
   - `capture` : Capturer la sortie d'un worker
   - `list` : Lister les workers actifs
   - `kill` / `kill-all` : Terminer les workers

2. **context-cli** - Gestion des rôles et contextes
   - Rôles YAML (prophet-claude.yaml, worker.yaml, manager.yaml)
   - Directives modulaires réutilisables
   - Génération de settings.json pour les permissions

3. **tickets-cli** - Système de tickets asynchrone
   - Création/gestion de tickets
   - Assignation aux workers
   - Notifications et ACK

4. **Système de persistance**
   - CLAUDE.md pour le contexte initial
   - Mémoires canoniques par Claude nommé
   - roles/ et directives/ pour la configuration

---

## Scope

### In Scope

- [ ] **Phase 1 : claude-cli** (MVP)
  - Spawn workers Claude dans tmux
  - Capture de la sortie des workers
  - Liste et kill des sessions
  - Auto-exit des workers

- [ ] **Phase 2 : context-cli**
  - Structure roles/ et directives/
  - Commande `show <role>` pour afficher le contexte
  - Génération settings.json
  - Rôles de base : prophet-claude, worker

- [ ] **Phase 3 : tickets-cli**
  - CRUD tickets
  - Assignation workers
  - États : open, in-progress, blocked, done

- [ ] **Phase 4 : Intégration**
  - Scripts de démarrage (restart-claude.sh)
  - Workflow Prophet → Worker
  - Documentation complète

### Out of Scope (v1)

- Voice control (FastAPI + Whisper)
- Streaming Twitch
- Git worktrees pour isolation
- Managers avancés (middle-manager, stream-manager)

---

## User Flow

### Flow Principal

1. Développeur lance Prophet Claude avec `./restart-prophet-claude.sh`
2. Prophet Claude reçoit une tâche complexe
3. Prophet délègue via `claude-cli spawn --role worker "Implémenter X"`
4. Worker s'exécute de manière autonome dans sa session tmux
5. Prophet vérifie la progression via `claude-cli capture <worker>`
6. Worker termine et sort automatiquement (auto-exit)
7. Prophet intègre le résultat et continue

### Exemple Concret

```bash
# Prophet reçoit : "Ajoute un système d'authentification"

# Prophet délègue :
claude-cli spawn --role worker --name auth-worker \
  "Implémente l'authentification JWT dans /src/auth.
   Crée les endpoints login/logout/refresh."

# Prophet continue sur autre chose...

# Plus tard, Prophet vérifie :
claude-cli capture auth-worker --lines 50

# Si terminé, Prophet intègre le travail
```

---

## Acceptance Criteria

### claude-cli

- [ ] `spawn` crée une session tmux avec Claude en mode interactif
- [ ] `spawn --role <role>` applique le contexte du rôle
- [ ] `spawn --name <name>` permet de nommer la session
- [ ] `capture <session> --lines N` affiche les N dernières lignes
- [ ] `list` affiche toutes les sessions claude-* actives
- [ ] `kill <session>` termine proprement une session
- [ ] `kill-all` termine toutes les sessions claude-*
- [ ] Les workers peuvent auto-exit avec `/exit`
- [ ] Les prompts sont envoyés via `tmux send-keys`

### context-cli

- [ ] Structure `roles/*.yaml` et `directives/*.yaml`
- [ ] `show <role>` combine le prompt + directives
- [ ] `list-roles` affiche les rôles disponibles
- [ ] `list-directives` affiche les directives
- [ ] `settings <role>` génère un settings.json valide
- [ ] Rôle `prophet-claude` défini avec contraintes
- [ ] Rôle `worker` défini pour les tâches déléguées

### tickets-cli

- [ ] `create <title> --body <description>` crée un ticket
- [ ] `list` affiche les tickets avec leur état
- [ ] `show <ticket-id>` affiche le détail
- [ ] `assign <ticket-id> <worker>` assigne un worker
- [ ] `update <ticket-id> --status <status>` change l'état
- [ ] États supportés : open, in-progress, blocked, done

### Intégration

- [ ] Script `restart-prophet-claude.sh` fonctionnel
- [ ] Prophet Claude peut spawner des workers
- [ ] Workers reçoivent le bon contexte via `--role`
- [ ] Documentation README pour chaque CLI

---

## Technical Notes

### Stack Technique

- **Python 3.11+** avec **uv** pour la gestion des dépendances
- **Click** pour les CLIs
- **tmux** pour l'isolation des sessions
- **YAML** pour la configuration des rôles

### Structure des Dossiers

```
bootstrap/
├── claude-cli/
│   ├── pyproject.toml
│   ├── main.py
│   └── README.md
├── context-cli/
│   ├── pyproject.toml
│   ├── main.py
│   ├── roles/
│   │   ├── prophet-claude.yaml
│   │   └── worker.yaml
│   ├── directives/
│   │   ├── base.yaml
│   │   └── persistent-memory.yaml
│   └── README.md
├── tickets-cli/
│   ├── pyproject.toml
│   ├── main.py
│   ├── tickets/          # Stockage JSON/YAML
│   └── README.md
├── CLAUDE.md             # Contexte Prophet (peut être vide si context-cli)
├── restart-prophet-claude.sh
└── memories/             # Mémoires persistantes par Claude
```

### Commandes tmux Clés

```bash
# Créer session
tmux new-session -d -s <name> "claude"

# Envoyer prompt
tmux send-keys -t <name> "prompt text" Enter

# Capturer sortie
tmux capture-pane -t <name> -p | tail -n 50

# Lister sessions
tmux list-sessions | grep "^claude-"

# Tuer session
tmux kill-session -t <name>
```

### Format Rôle YAML

```yaml
# roles/worker.yaml
name: worker
description: Worker Claude for delegated tasks
prompt: |
  You are a Worker Claude. Complete the assigned task and exit.

  CONSTRAINTS:
  - Focus on the specific task given
  - Do not start new tasks
  - Exit when done with /exit

directives:
  - base
  - code-quality
```

### Sécurité

- Ne jamais exposer les clés API dans les logs
- Isoler chaque worker dans sa propre session tmux
- Permissions restrictives via settings.json
- Rate limiting pour éviter les spawns excessifs

---

## Dependencies

### Prérequis Système

- tmux installé et configuré
- Python 3.11+ avec uv
- Claude Code CLI installé et configuré
- Compte Claude avec crédits suffisants

### Dépendances Python

```toml
[dependencies]
click = "^8.1"
pyyaml = "^6.0"
```

### Ordre d'Implémentation

1. **claude-cli** (aucune dépendance)
2. **context-cli** (aucune dépendance)
3. **tickets-cli** (optionnel, peut utiliser context-cli pour les rôles)
4. **Intégration** (dépend des 3 CLIs)

---

## Definition of Done

- [ ] Code implémenté et commité
- [ ] Tests manuels passés pour chaque commande
- [ ] README documenté pour chaque CLI
- [ ] Workflow complet testé : Prophet → spawn → capture → intégration
- [ ] Au moins 2 rôles définis (prophet-claude, worker)
- [ ] Script restart-prophet-claude.sh fonctionnel
- [ ] Pas d'erreurs lors de l'exécution normale

---

## Story Points Breakdown

| Composant | Points | Complexité |
|-----------|--------|------------|
| claude-cli | 5 | Moyenne - tmux + Click |
| context-cli | 3 | Simple - YAML + templating |
| tickets-cli | 3 | Simple - CRUD basique |
| Intégration | 2 | Simple - scripts shell |
| **Total** | **13** | |

**Rationale:** Le système complet est trop gros pour une seule story. Recommandation : décomposer en 4 sous-stories (une par composant).

---

## Sous-Stories

| ID | Titre | Points | Priorité | Dépendances |
|----|-------|--------|----------|-------------|
| [STORY-001a](STORY-001a.md) | Implémenter claude-cli | 5 | Must Have | - |
| [STORY-001b](STORY-001b.md) | Implémenter context-cli | 3 | Should Have | 001a |
| [STORY-001c](STORY-001c.md) | Implémenter tickets-cli | 3 | Could Have | 001a |
| [STORY-001d](STORY-001d.md) | Intégration et documentation | 2 | Must Have | 001a, 001b |

### Ordre d'implémentation recommandé

```
STORY-001a (claude-cli)     ──────┐
         │                        │
         ▼                        ▼
STORY-001b (context-cli)    STORY-001c (tickets-cli)
         │                        │
         └────────┬───────────────┘
                  ▼
         STORY-001d (intégration)
```

---

## Ressources

- **Tutoriel extrait** : `tutorial.md` (488 Ko, 362 frames analysées)
- **Vidéo source** : https://www.twitch.tv/claudecodeonly/video/2657952550
- **Frames** : `/tmp/claude/.../twitch_frames/frames/` (4344 images)

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée

**Actual Effort:** TBD

---

**Cette story a été créée en suivant le tutoriel Multi-Claude Bootstrap de @claudecodeonly**
