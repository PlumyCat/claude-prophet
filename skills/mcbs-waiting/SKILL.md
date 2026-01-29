---
name: mcbs-waiting
description: Signal que le worker attend une réponse de Prophet
allowed-tools: Bash, Read, Write
---

# Waiting - Attente de réponse Prophet

Ce skill permet à un worker de signaler qu'il a besoin d'une réponse de Prophet Claude avant de continuer.

## Utilisation

```
/mcbs:waiting "Ta question pour Prophet"
```

## Paramètres

1. **Message** (requis) : La question ou demande pour Prophet
2. **Ticket ID** (optionnel) : Si pas fourni, essaie de le détecter depuis le contexte

## Actions à effectuer

### 1. Identifier la session et le ticket

```bash
# Récupérer le nom de la session tmux courante
tmux display-message -p '#S'
```

Si le ticket ID n'est pas connu, demander à l'utilisateur ou chercher dans le contexte.

### 2. Mettre à jour le ticket en status "waiting"

```bash
/home/eric/projects/twich-test/tickets update <ticket-id> --status waiting
/home/eric/projects/twich-test/tickets comment <ticket-id> "Waiting for Prophet: <message>"
```

### 3. Créer le fichier signal

Écrire le fichier JSON dans `/home/eric/projects/twich-test/signals/waiting/<session>.json`:

```json
{
  "session": "<session-name>",
  "ticket_id": "<ticket-id>",
  "timestamp": "<ISO-8601>",
  "message": "<question pour Prophet>",
  "type": "question"
}
```

Commande pour créer le fichier (remplacer les variables):
```bash
cat > /home/eric/projects/twich-test/signals/waiting/<session>.json << 'EOF'
{
  "session": "<session>",
  "ticket_id": "<ticket-id>",
  "timestamp": "<timestamp>",
  "message": "<message>",
  "type": "question"
}
EOF
```

### 4. Attendre la réponse (polling)

Vérifier périodiquement si une réponse existe:

```bash
# Vérifier si réponse disponible
ls /home/eric/projects/twich-test/signals/responses/<session>.json 2>/dev/null
```

Si le fichier existe, lire la réponse:
```bash
cat /home/eric/projects/twich-test/signals/responses/<session>.json
```

### 5. Traiter la réponse

Une fois la réponse reçue:
1. Lire et afficher la réponse de Prophet
2. Supprimer le fichier signal waiting (Prophet l'a déjà fait normalement)
3. Continuer le travail avec la réponse

## Format du signal waiting

```json
{
  "session": "claude-auth",
  "ticket_id": "abc123",
  "timestamp": "2026-01-29T14:30:00Z",
  "message": "OAuth ou JWT pour l'authentification?",
  "type": "question"
}
```

## Format de la réponse (signals/responses/)

```json
{
  "session": "claude-auth",
  "ticket_id": "abc123",
  "timestamp": "2026-01-29T14:35:00Z",
  "response": "Utilise OAuth2 avec refresh tokens",
  "from": "prophet"
}
```

## Workflow

```
Worker a une question
       │
       ▼
  /mcbs:waiting "OAuth ou JWT?"
       │
       ├─► tickets update → waiting
       ├─► Écrit signals/waiting/<session>.json
       │
       ▼
  Worker attend (poll responses/)
       │
       ▼
  Prophet voit via /mcbs:status
       │
       ▼
  Prophet répond via /mcbs:respond
       │
       ▼
  Worker lit la réponse
       │
       ▼
  Continue le travail
```

## Notes importantes

- **NE PAS** faire `/exit` pendant l'attente
- **NE PAS** continuer avec des suppositions - attendre la réponse
- Si bloqué trop longtemps, mettre le ticket en `blocked` au lieu de `waiting`
- Prophet sera notifié via `/mcbs:status` des workers en attente
