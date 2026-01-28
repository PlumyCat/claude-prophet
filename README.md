# Claude Prophet - Multi-Claude Bootstrap System

Système d'orchestration multi-agents Claude permettant de déléguer des tâches à des workers isolés dans des sessions tmux.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                     HUMAN                           │
│                       │                             │
│                       ▼                             │
│  ┌─────────────────────────────────────────────┐    │
│  │             PROPHET CLAUDE                  │    │
│  │            (Orchestrateur)                  │    │
│  │                                             │    │
│  │  • Reçoit les demandes                      │    │
│  │  • Délègue aux workers                      │    │
│  │  • Supervise et intègre                     │    │
│  └─────────────────────────────────────────────┘    │
│                       │                             │
│          ┌────────────┼────────────┐                │
│          ▼            ▼            ▼                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │  WORKER 1  │ │  WORKER 2  │ │  WORKER N  │       │
│  │   (tmux)   │ │   (tmux)   │ │   (tmux)   │       │
│  └────────────┘ └────────────┘ └────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Installation

### Prérequis

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets Python)
- tmux
- Claude Code CLI configuré

### Setup

```bash
git clone https://github.com/PlumyCat/claude-prophet.git
cd claude-prophet

# Installer les dépendances de chaque CLI
cd claude-cli && uv sync && cd ..
cd context-cli && uv sync && cd ..
cd tickets-cli && uv sync && cd ..

# Installer les skills Claude Code (MCBS)
./install-skills.sh
```

## Quick Start

```bash
# 1. Démarrer Prophet Claude
./restart-prophet-claude.sh

# 2. Attacher la session
tmux attach -t prophet-claude

# 3. Dans Prophet Claude, déléguer une tâche
./claude spawn --role worker --name my-task "Implémenter une fonction fibonacci"

# 4. Vérifier le worker
./claude list
./claude capture my-task
```

## Composants

### claude-cli

Gestion des workers tmux.

```bash
./claude spawn "prompt"              # Spawn un worker
./claude spawn --name foo "prompt"   # Avec un nom
./claude spawn --role worker "prompt" # Avec un rôle
./claude capture foo --lines 50      # Voir la sortie
./claude list                        # Lister les workers
./claude kill foo                    # Tuer un worker
./claude kill-all                    # Tuer tous les workers
```

### context-cli

Gestion des rôles et directives.

```bash
./context list-roles        # Lister les rôles
./context list-directives   # Lister les directives
./context show worker       # Afficher le contexte d'un rôle
./context settings worker   # Générer settings.json
./context validate worker   # Valider un rôle
```

### tickets-cli

Tracking des tâches déléguées.

```bash
./tickets create "Task"      # Créer un ticket
./tickets list               # Lister les tickets
./tickets show abc123        # Voir un ticket
./tickets assign abc123 worker # Assigner un worker
./tickets update abc123 --status done # Marquer comme terminé
./tickets stats              # Statistiques
```

## Structure

```
claude-prophet/
├── claude                    # Wrapper → claude-cli
├── context                   # Wrapper → context-cli
├── tickets                   # Wrapper → tickets-cli
├── restart-prophet-claude.sh # Script de démarrage
├── install-skills.sh         # Installe les skills MCBS
├── claude-cli/               # CLI gestion workers
├── context-cli/              # CLI gestion contextes
│   ├── roles/                # Définitions des rôles
│   └── directives/           # Directives réutilisables
├── tickets-cli/              # CLI tracking des tâches
│   └── tickets/              # Stockage JSON des tickets
├── skills/mcbs/              # Skills Claude Code (MCBS)
│   ├── prophet/              # Gestion Prophet Claude
│   ├── spawn/                # Spawner un worker
│   ├── workers/              # Lister les workers
│   ├── capture/              # Capturer la sortie
│   ├── kill/                 # Tuer les workers
│   ├── status/               # Status système
│   ├── ticket/               # Gestion tickets
│   └── done/                 # Signaler fin de tâche
└── docs/
    ├── GUIDE.md              # Guide d'utilisation complet
    └── stories/              # User stories
```

## Skills Claude Code (MCBS)

Skills globaux disponibles depuis n'importe quel projet (`~/.claude/skills/mcbs/`).

| Skill | Description |
|-------|-------------|
| `/mcbs:prophet` | (Re)lancer Prophet Claude dans tmux |
| `/mcbs:spawn` | Créer un worker avec options |
| `/mcbs:workers` | Lister les workers actifs |
| `/mcbs:capture` | Voir la sortie d'un worker |
| `/mcbs:kill` | Tuer un/tous les workers |
| `/mcbs:status` | Vue d'ensemble système |
| `/mcbs:ticket` | Gestion des tickets |
| `/mcbs:done` | Signaler fin de tâche (workers) |

### Exemple d'utilisation

```bash
# Depuis n'importe quel terminal avec Claude Code
claude

# Dans Claude
> /mcbs:status           # Voir l'état du système
> /mcbs:spawn            # Créer un worker (interactif)
> /mcbs:workers          # Lister les workers
> /mcbs:capture worker-1 # Voir la sortie
```

## Documentation

- [Guide d'utilisation complet](docs/GUIDE.md)
- [claude-cli README](claude-cli/README.md)
- [context-cli README](context-cli/README.md)
- [tickets-cli README](tickets-cli/README.md)

## Comment ce projet a été créé

Ce projet a été généré automatiquement à partir d'une vidéo Twitch de 6h grâce à un pipeline "Video-to-Code" :

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Vidéo Twitch   │────▶│ Extraction      │────▶│ Analyse frames  │
│  (6h, no audio) │     │ frames (ffmpeg) │     │ (GPT-4 Vision)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Code    │◀────│ BMAD Stories    │◀────│ Tutoriel MD     │
│  Implementation │     │ (User Stories)  │     │ (documentation) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Étapes

1. **Téléchargement** : `yt-dlp` pour récupérer la vidéo Twitch
2. **Extraction frames** : `ffmpeg -vf "fps=1/5"` → 4344 frames
3. **Analyse vision** : Azure OpenAI GPT-4.1-mini analyse les frames
4. **Génération tutoriel** : Documentation structurée en Markdown
5. **BMAD Stories** : Conversion en User Stories avec le workflow BMAD
6. **Implémentation** : Claude Code implémente chaque story

### Résultat

Une vidéo de 6h transformée en système fonctionnel avec :
- 3 CLIs (claude-cli, context-cli, tickets-cli)
- 8 skills Claude Code
- Architecture multi-agents complète

## Crédits

Basé sur le tutoriel Multi-Claude Bootstrap de [@claudecodeonly](https://www.twitch.tv/claudecodeonly).

Un grand merci pour cette vidéo Twitch de 6h qui présente un système d'orchestration multi-agents vraiment innovant. L'approche avec Prophet Claude, les workers tmux, et le système de tickets est élégante et puissante.

Vidéo source : https://www.twitch.tv/claudecodeonly/video/2657952550

## Licence

MIT
