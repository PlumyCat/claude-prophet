---
name: mcbs-respond
description: Répondre à un worker en attente
allowed-tools: Bash, Read, Write
---

# Respond - Répondre à un worker en attente

Ce skill permet à Prophet Claude de répondre à un worker qui attend une réponse via `/mcbs:waiting`.

## Utilisation

```
/mcbs:respond <session> "Ta réponse"
```

## Paramètres

1. **Session** (requis) : Nom de la session tmux du worker (ex: `claude-auth`)
2. **Response** (requis) : La réponse à envoyer au worker

## Actions à effectuer

### 1. Vérifier le signal waiting

```bash
cat /home/eric/projects/twich-test/signals/waiting/<session>.json
```

Cela donne le contexte: ticket_id, message original, timestamp.

### 2. Écrire la réponse

Créer le fichier `/home/eric/projects/twich-test/signals/responses/<session>.json`:

```json
{
  "session": "<session>",
  "ticket_id": "<ticket-id-from-waiting>",
  "timestamp": "<ISO-8601>",
  "response": "<ta réponse>",
  "from": "prophet"
}
```

Commande:
```bash
cat > /home/eric/projects/twich-test/signals/responses/<session>.json << 'EOF'
{
  "session": "<session>",
  "ticket_id": "<ticket-id>",
  "timestamp": "<timestamp>",
  "response": "<réponse>",
  "from": "prophet"
}
EOF
```

### 3. Mettre à jour le ticket

```bash
/home/eric/projects/twich-test/tickets update <ticket-id> --status in-progress
/home/eric/projects/twich-test/tickets comment <ticket-id> "Prophet responded: <résumé>"
```

### 4. Envoyer le message au worker

```bash
/home/eric/projects/twich-test/claude send <session> "Prophet: <ta réponse>"
```

### 5. Supprimer le signal waiting

```bash
rm /home/eric/projects/twich-test/signals/waiting/<session>.json
```

## Workflow complet

```
Prophet voit worker waiting (via /mcbs:status)
       │
       ▼
  /mcbs:respond claude-auth "Utilise OAuth2"
       │
       ├─► Lit signals/waiting/claude-auth.json
       ├─► Écrit signals/responses/claude-auth.json
       ├─► tickets update → in-progress
       ├─► ./claude send claude-auth "Prophet: ..."
       ├─► rm signals/waiting/claude-auth.json
       │
       ▼
  Worker reçoit la réponse
       │
       ▼
  Worker continue le travail
```

## Exemple

```bash
# Voir les workers en attente
/mcbs:status

# Output montre:
# ⏳ Workers en attente:
#   claude-auth: "OAuth ou JWT?" (depuis 5 min)

# Répondre
/mcbs:respond claude-auth "Utilise OAuth2 avec refresh tokens. Voir la doc dans /docs/auth.md"
```

## Voir les workers en attente

Pour lister les workers en attente:

```bash
ls -la /home/eric/projects/twich-test/signals/waiting/

# Voir le détail d'un signal
cat /home/eric/projects/twich-test/signals/waiting/<session>.json
```

Ou utiliser `/mcbs:status` qui affiche cette section.

## Notes

- Toujours répondre aux workers en attente rapidement
- La réponse est envoyée via `./claude send` pour notification immédiate
- Le fichier responses/ sert de backup si le send échoue
- Le ticket repasse automatiquement en `in-progress`
