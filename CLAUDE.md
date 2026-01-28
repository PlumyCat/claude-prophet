# Twitch Tutorial Extractor

Projet d'extraction de tutoriels vidéo Twitch (sans audio) en documentation textuelle.

## Contexte

Ce projet extrait le contenu de vidéos tutorielles en utilisant:
1. **ffmpeg** pour extraire les frames de la vidéo
2. **Azure OpenAI GPT-4.1-mini** (vision) pour analyser les frames et extraire le texte

## Source vidéo

Tutoriel Twitch de @claudecodeonly sur la création d'un système **Multi-Claude Bootstrap**:
- URL: https://www.twitch.tv/claudecodeonly/video/2657952550
- Durée: ~6 heures
- Contenu: Système d'orchestration multi-agents Claude avec tmux

## Structure

```
twich-test/
├── .env                    # Credentials Azure (NE PAS COMMITER)
├── .gitignore
├── requirements.txt
├── extract_frames.py       # Script principal d'extraction
├── CLAUDE.md              # Ce fichier
└── output/                # Résultats d'extraction (généré)
```

## Utilisation

### 1. Télécharger la vidéo et extraire les frames

```bash
# Télécharger
yt-dlp -o video.mp4 "https://www.twitch.tv/claudecodeonly/video/2657952550"

# Extraire frames (1 toutes les 5 secondes)
mkdir -p frames
ffmpeg -i video.mp4 -vf "fps=1/5" -q:v 2 frames/frame_%05d.jpg
```

### 2. Extraire le contenu avec Azure

```bash
# Installer les dépendances
pip install -r requirements.txt

# Extraire (1 frame par minute par défaut)
python extract_frames.py --frames-dir ./frames --output tutorial.md

# Options
python extract_frames.py \
  --frames-dir ./frames \
  --output tutorial.md \
  --sample-rate 6 \        # 1 frame toutes les 30 sec
  --start-frame 100 \      # Commencer à la frame 100
  --end-frame 500          # Finir à la frame 500
```

## Configuration Azure

Le fichier `.env` contient:
- `AZURE_OPENAI_ENDPOINT`: Endpoint Azure Foundry
- `AZURE_OPENAI_API_KEY`: Clé API
- `AZURE_OPENAI_DEPLOYMENT`: Nom du déploiement (gpt-4.1-mini)

## Contenu du tutoriel (résumé préliminaire)

Le tutoriel couvre la création d'un système multi-agents Claude:

### Architecture
- **Prophet Claude**: Orchestrateur principal, interface humaine
- **Workers**: Agents délégués dans des sessions tmux séparées
- **Managers**: Middle-manager, stream-manager pour la coordination

### Composants
- `claude-cli`: CLI Python pour spawner/gérer les workers
- `context-cli`: Gestion des rôles et directives
- `tickets-cli`: Système de tickets pour tracker les tâches

### Concepts clés
- Sessions tmux pour isoler les workers
- CLAUDE.md pour la persistance du contexte
- Rôles YAML (prophet-claude.yaml, worker.yaml)
- Directives modulaires réutilisables
- Named Claudes avec mémoires canoniques

## Frames source

Les frames extraites sont stockées dans:
```
/tmp/claude/-home-eric-cc-config/07a4be6d-7f6d-4615-9097-be0ecb6f02c7/scratchpad/twitch_frames/frames/
```

Total: 4344 frames (~6h de vidéo à 5 sec d'intervalle)
